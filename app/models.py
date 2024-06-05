from app.db import db  # Import the db instance

class VM(db.Model):
    __tablename__ = 'vms'
    id = db.Column(db.Integer, primary_key=True)
    vm_id = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    tags = db.Column(db.String, nullable=True)

class FirewallRule(db.Model):
    __tablename__ = 'firewall_rules'
    id = db.Column(db.Integer, primary_key=True)
    fw_id = db.Column(db.String, unique=True, nullable=False)
    source_tag = db.Column(db.String, nullable=False)
    dest_tag = db.Column(db.String, nullable=False)
