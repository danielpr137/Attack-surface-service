from flask import current_app, jsonify, request, abort
from app import app, db
from app.models import VirtualMachine
from app.cloud_env import get_attackers
from app.utils import timed_function

# Global variables to store statistics
request_count = 0
total_request_time = 0

@app.route('/api/v1/attack', methods=['GET'])
# @timed_function
def attack(execution_time=None):
    global request_count, total_request_time
    vm_id = request.args.get('vm_id')
    app.logger.info(f'Received attack request for VM ID: {vm_id}')

    attackers, error_message = get_attackers(vm_id)
    if error_message:
        app.logger.warning(error_message)
        abort(404, error_message)

    request_count += 1
    total_request_time += execution_time or 0  # Add the execution time to the total

    if attackers:
        app.logger.info(f'Found {len(attackers)} attackers for VM ID: {vm_id}')
    else:
        app.logger.warning(f'No attackers found for VM ID: {vm_id}')

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