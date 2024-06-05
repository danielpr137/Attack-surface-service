from app import app, db
from app.models import VirtualMachine
from app.cloud_env import get_attackers
from app.utils import get_attackers
from flask import Blueprint, request, jsonify, current_app


# Global variables to store statistics
request_count = 0
total_request_time = 0


api_bp = Blueprint('api', __name__)

@api_bp.route('/attack', methods=['GET'])
def attack():
    vm_id = request.args.get('vm_id')
    cloud_env = current_app.config['cloud_env']
    attackers = get_attackers(vm_id, cloud_env)
    return jsonify(attackers)

@app.route('/api/v1/stats', methods=['GET'])
def stats(execution_time=None):
    global request_count, total_request_time
    average_request_time = total_request_time / request_count if request_count > 0 else 0

    with current_app.app_context():
        vm_count = db.session.query(VirtualMachine).count()

    request_count += 1
    total_request_time += execution_time or 0  # Add the execution time to the total

    return jsonify({
        'vm_count': vm_count,
        'request_count': request_count,
        'average_request_time': average_request_time
    })