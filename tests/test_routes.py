import os
import rastrea2r_server
from rastrea2r_server import app, auth, config, db, user
import unittest
from base64 import b64encode
from flask import jsonify


class RoutesTestCase(unittest.TestCase):
    TEST_USER = "testuser"
    TEST_PWD = "testpasswd"

    def setUp(self):
        rastrea2r_server.app.config["TESTING"] = True
        app.config["DEBUG"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
            app.root_path, "testdb"
        )
        self.app = app.test_client()
        db.drop_all()
        db.create_all()
        user.add_user(self.TEST_USER, self.TEST_PWD)

    # executed after each test
    def tearDown(self):
        pass

    def test_del_method_not_allowed_on_rule(self):
        headers = {
            "Authorization": "Basic %s"
            % b64encode(b"testuser:testpasswd").decode("ascii")
        }
        response = self.app.delete("/rastrea2r/api/v1.0/rule", headers=headers)
        self.assertIn(b"Method Not Allowed", response.data)
        self.assertEqual(response.status_code, 405)

    def test_missing_rulename(self):
        headers = {
            "Authorization": "Basic %s"
            % b64encode(b"testuser:testpasswd").decode("ascii")
        }
        response = self.app.get("/rastrea2r/api/v1.0/rule", headers=headers)
        self.assertIn(b"Not Found: description : Invalid Rule Requested", response.data)
        self.assertEqual(response.status_code, 404)

    def test_invalid_rulename(self):
        headers = {
            "Authorization": "Basic %s"
            % b64encode(b"testuser:testpasswd").decode("ascii")
        }
        response = self.app.get(
            "/rastrea2r/api/v1.0/rule?rulename=invalidrule", headers=headers
        )
        self.assertIn(b"Not Found: description : Invalid Rule Requested", response.data)
        self.assertEqual(response.status_code, 404)

    def test_valid_rulename(self):
        headers = {
            "Authorization": "Basic %s"
            % b64encode(b"testuser:testpasswd").decode("ascii")
        }
        response = self.app.get(
            "/rastrea2r/api/v1.0/rule?rulename=example.yara", headers=headers
        )
        self.assertIn(b"This will match any file containing", response.data)
        self.assertEqual(response.status_code, 200)

    def test_post_result(self):
        sample_data = [
            {
                "rulename": "rule1",
                "filename": "rule1.txt",
                "hostname": "CAAT9199XXXX",
                "module": "testmodule1",
            },
            {
                "rulename": "rule2",
                "filename": "rule2.txt",
                "hostname": "CAAT9199XXXX",
                "module": "testmodule2",
            },
        ]

        headers = {
            "Authorization": "Basic %s"
            % b64encode(b"testuser:testpasswd").decode("ascii"),
            "Content-Type": "application/json",
        }
        invalid_headers = {
            "Authorization": "Basic %s"
            % b64encode(b"testuser:testpasswd").decode("ascii"),
            "Content-Type": "text/html",
        }
        response = self.app.post(
            "/rastrea2r/api/v1.0/results", headers=headers, json=sample_data
        )
        self.assertIn(b"Results Saved Successfully", response.data)
        self.assertEqual(response.status_code, 200)
        response = self.app.post(
            "/rastrea2r/api/v1.0/results", headers=headers, data="aa"
        )
        self.assertIn(b"Bad Request", response.data)
        self.assertEqual(response.status_code, 400)
