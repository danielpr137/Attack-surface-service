import unittest
from app import create_app, db
from app.models import VM, FirewallRule

class StatsTestCase(unittest.TestCase):
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

    def test_stats(self):
        response = self.client.get('/api/v1/stats')
        self.assertEqual(response.status_code, 200)
        self.assertIn('vm_count', response.json)
        self.assertIn('request_count', response.json)
        self.assertIn('average_request_time', response.json)

if __name__ == '__main__':
    unittest.main()
