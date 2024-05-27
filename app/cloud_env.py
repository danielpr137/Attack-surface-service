import json
from app import app

def load_cloud_env(file_path):
    """Load the cloud environment from the provided JSON file."""
    global cloud_env, vm_count
    with open(file_path, 'r') as f:
        cloud_env = json.load(f)
    # vm_count = len(cloud_env['vms'])
    vm_count = 3
    with open("stats.json", "w") as f:
        json.dump(
            {
                "vm_count": len(cloud_env['vms']),
                "request_count": 0,
                "total_request_time": 0
            },
            f,
            indent=2
        )

def get_attackers(vm_id):
    """Get the list of virtual machine IDs that can attack the given VM."""
    from app.utils import can_attack
    try:
        target_vm = next((vm for vm in cloud_env['vms'] if vm['vm_id'] == vm_id), None)
        if not target_vm:
            raise ValueError(f'VM ID {vm_id} not found in the cloud environment')
        attackers = []
        target_tags = target_vm['tags']
        for vm in cloud_env['vms']:
            if vm['vm_id'] != vm_id and can_attack(vm['tags'], target_tags, cloud_env['fw_rules']):
                attackers.append(vm['vm_id'])
        return attackers, None
    except ValueError as e:
        return None, str(e)

def save_stats(**kwargs):
    pass