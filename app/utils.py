import time

def can_attack(attacker_tags, target_tags, fw_rules):
    """Check if the attacker can access the target based on the firewall rules."""
    for rule in fw_rules:
        if rule.source_tag in attacker_tags and rule.dest_tag in target_tags:
            return True
    return False

def timed_function(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        return result, execution_time
    return wrapper