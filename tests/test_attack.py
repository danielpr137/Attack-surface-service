import unittest
from app import create_app, db
from app.models import VM, FirewallRule

class AttackTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

        with self.app.app_context():
            db.create_all()

            vm1 = VM(vm_id="vm-a211de", name="jira_server", tags="ci,dev")
            vm2 = VM(vm_id="vm-c7bac01a07", name="bastion", tags="ssh,dev")
            db.session.add(vm1)
            db.session.add(vm2)

            rule = FirewallRule(fw_id="fw-82af742", source_tag="ssh", dest_tag="dev")
            db.session.add(rule)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_attack(self):
        response = self.client.get('/api/v1/attack?vm_id=vm-a211de')
        self.assertEqual(response.status_code, 200)
        self.assertIn("vm-c7bac01a07", response.json)

    def test_attack_missing_vm_id(self):
        response = self.client.get('/api/v1/attack')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['error'], "vm_id parameter is required")

    def test_attack_invalid_vm_id(self):
        response = self.client.get('/api/v1/attack?vm_id=invalid')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], "vm_id 'invalid' not found")

if __name__ == '__main__':
    unittest.main()
