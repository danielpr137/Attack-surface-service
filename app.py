from flask import Flask, request, jsonify
import time
import json
import sys
from app.routes import api_bp

app = Flask(__name__)
app.register_blueprint(api_bp, url_prefix='/api/v1')

# Global variables to track statistics
request_count = 0
total_request_time = 0
vm_count = 0
cloud_env = {}

def load_environment(file_path):
    global cloud_env, vm_count
    with open(file_path) as f:
        cloud_env = json.load(f)
        vm_count = len(cloud_env['vms'])
    app.config['cloud_env'] = cloud_env

@app.before_request
def start_timer():
    request.start_time = time.time()

@app.after_request
def log_request(response):
    global request_count, total_request_time
    request_count += 1
    total_request_time += (time.time() - request.start_time)
    return response

@app.route('/api/v1/stats', methods=['GET'])
def stats():
    global request_count, total_request_time, vm_count
    average_request_time = (total_request_time / request_count) if request_count > 0 else 0
    return jsonify({
        "vm_count": vm_count,
        "request_count": request_count,
        "average_request_time": average_request_time
    })

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python app.py <path_to_input_json>")
        sys.exit(1)
    
    input_file = sys.argv[1]
    load_environment(f'inputs/{input_file}')
    app.run(debug=True)
