def get_vm_ids(cloud_env):
    return [vm['vm_id'] for vm in cloud_env['vms']]

def get_attackers(vm_id, cloud_env):
    attackers = []
    vm_tags = {vm['vm_id']: vm['tags'] for vm in cloud_env['vms']}
    fw_rules = cloud_env['fw_rules']

    if vm_id not in vm_tags:
        return None

    dest_tags = set(vm_tags[vm_id])

    for rule in fw_rules:
        if rule['dest_tag'] in dest_tags:
            source_tag = rule['source_tag']
            for vm in cloud_env['vms']:
                if source_tag in vm['tags'] and vm['vm_id'] != vm_id:
                    attackers.append(vm['vm_id'])

    return attackers
