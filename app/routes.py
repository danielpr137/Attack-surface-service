from flask import jsonify, request, abort
import time
from app import app
from app.cloud_env import load_cloud_env, get_attackers
from app.utils import can_attack

# Global variables to store cloud environment and statistics
cloud_env = None
vm_count = 0
request_count = 0
total_request_time = 0


@app.route('/')
def index():
    return 'Hey Orca!'

@app.route('/api/v1/attack', methods=['GET'])
def attack():
    vm_id = request.args.get('vm_id')
    app.logger.info(f'Received attack request for VM ID: {vm_id}')

    attackers, error_message = get_attackers(vm_id)
    if error_message:
        app.logger.warning(error_message)
        abort(404, error_message)

    if attackers:
        app.logger.info(f'Found {len(attackers)} attackers for VM ID: {vm_id}')
    else:
        app.logger.warning(f'No attackers found for VM ID: {vm_id}')

    return jsonify(attackers)

@app.route('/api/v1/stats', methods=['GET'])
def stats():
    app.logger.info('Received stats request')
    global request_count, total_request_time, vm_count
    average_request_time = total_request_time / request_count if request_count > 0 else 0
    return jsonify({
        'vm_count': vm_count,
        'request_count': request_count,
        'average_request_time': average_request_time
    })

