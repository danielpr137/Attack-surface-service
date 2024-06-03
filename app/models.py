from app import db

class VirtualMachine(db.Model):
    __tablename__ = 'virtual_machines'

    vm_id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String)
    tags = db.Column(db.JSON)

    def __repr__(self):
        return f'<VirtualMachine {self.vm_id}>'

class FirewallRule(db.Model):
    __tablename__ = 'firewall_rules'

    fw_id = db.Column(db.String, primary_key=True)
    source_tag = db.Column(db.String)
    dest_tag = db.Column(db.String)

    def __repr__(self):
        return f'<FirewallRule {self.fw_id}>'