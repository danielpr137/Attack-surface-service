from app import create_app, db
from app.models import VM, FirewallRule
import os
import json

def initialize_database():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        input_file = os.getenv('CLOUD_ENV_FILE')
        with open(input_file) as f:
            cloud_env = json.load(f)
            vms = cloud_env['vms']
            fw_rules = cloud_env['fw_rules']

            for vm in vms:
                existing_vm = VM.query.filter_by(vm_id=vm['vm_id']).first()
                if not existing_vm:
                    new_vm = VM(
                        vm_id=vm['vm_id'],
                        name=vm['name'],
                        tags=','.join(vm['tags'])
                    )
                    db.session.add(new_vm)

            for rule in fw_rules:
                existing_rule = FirewallRule.query.filter_by(fw_id=rule['fw_id']).first()
                if not existing_rule:
                    new_rule = FirewallRule(
                        fw_id=rule['fw_id'],
                        source_tag=rule['source_tag'],
                        dest_tag=rule['dest_tag']
                    )
                    db.session.add(new_rule)

            db.session.commit()

if __name__ == "__main__":
    initialize_database()
