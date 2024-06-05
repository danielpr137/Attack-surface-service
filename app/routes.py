from flask import Blueprint, request, jsonify, current_app
from app.utils import get_attackers
from app.models import VM, FirewallRule
import time
import logging

api_bp = Blueprint('api', __name__)

logger = logging.getLogger(__name__)

request_count = 0
total_request_time = 0

@api_bp.before_app_request
def start_timer():
    request.start_time = time.time()

@api_bp.after_app_request
def log_request(response):
    global request_count, total_request_time
    request_count += 1
    request_time = time.time() - request.start_time
    total_request_time += request_time
    logger.info(f"Processed request {request.path} in {request_time:.4f} seconds")
    return response

@api_bp.route('/attack', methods=['GET'])
def attack():
    vm_id = request.args.get('vm_id')
    if not vm_id:
        logger.warning("Missing vm_id parameter")
        return jsonify({"error": "vm_id parameter is required"}), 400

    vm = VM.query.filter_by(vm_id=vm_id).first()
    if not vm:
        logger.warning(f"vm_id '{vm_id}' not found")
        return jsonify({"error": f"vm_id '{vm_id}' not found"}), 404

    cloud_env = current_app.config['cloud_env']
    attackers = get_attackers(vm_id, cloud_env)

    logger.info(f"Retrieved attackers for vm_id '{vm_id}'")
    return jsonify(attackers)

@api_bp.route('/stats', methods=['GET'])
def stats():
    global request_count, total_request_time
    vm_count = current_app.config['vm_count']
    average_request_time = (total_request_time / request_count) if request_count > 0 else 0
    logger.info("Retrieved statistics")
    return jsonify({
        "vm_count": vm_count,
        "request_count": request_count,
        "average_request_time": average_request_time
    })

@api_bp.errorhandler(404)
def not_found(error):
    logger.error("404 Not Found")
    return jsonify({"error": "Not found"}), 404

@api_bp.errorhandler(500)
def internal_error(error):
    logger.error(f"500 Internal Server Error: {error}")
    return jsonify({"error": "Internal server error"}), 500
