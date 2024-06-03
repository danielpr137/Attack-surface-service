import json
from app.utils import can_attack
from flask import current_app
from app import db
from app.models import VirtualMachine, FirewallRule

def load_cloud_env(file_path):
    """Load the cloud environment from the provided JSON file."""
    global vm_count  # Declare vm_count as global within the function
    with current_app.app_context():
        with open(file_path, 'r') as f:
            cloud_env = json.load(f)

        # Clear existing data
        db.session.query(VirtualMachine).delete()
        db.session.query(FirewallRule).delete()

        # Insert new data
        for vm in cloud_env['vms']:
            db.session.add(VirtualMachine(vm_id=vm['vm_id'], name=vm['name'], tags=vm['tags']))

        for rule in cloud_env['fw_rules']:
            db.session.add(FirewallRule(fw_id=rule['fw_id'], source_tag=rule['source_tag'], dest_tag=rule['dest_tag']))

        db.session.commit()

def get_attackers(vm_id):
    """Get the list of virtual machine IDs that can attack the given VM."""
    with current_app.app_context():
        target_vm = db.session.query(VirtualMachine).filter_by(vm_id=vm_id).first()
        if not target_vm:
            return [], f'VM ID {vm_id} not found in the cloud environment'

        attackers = []
        target_tags = target_vm.tags
        fw_rules = db.session.query(FirewallRule).all()

        for vm in db.session.query(VirtualMachine).filter(VirtualMachine.vm_id != vm_id):
            if can_attack(vm.tags, target_tags, fw_rules):
                attackers.append(vm.vm_id)

        return attackers, None

def save_stats(**kwargs):
    pass