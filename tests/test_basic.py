
import os
import rastrea2r_server
from rastrea2r_server import app, auth, config, db, user
import unittest
from base64 import b64encode


class BasicTestCase(unittest.TestCase):
    """ Basic test cases """

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

    def test_basic(self):
        """ check True is True """
        self.assertTrue(True)

    def test_version(self):
        """ check rastrea2r_server exposes a version attribute """
        self.assertTrue(hasattr(rastrea2r_server, "__version__"))
        self.assertIsInstance(rastrea2r_server.__version__, str)

    def test_unauthenticate_api(self):
        response = self.app.get("/test")
        self.assertIn(b"Hello World", response.data)
        self.assertEqual(response.status_code, 200)

    def test_valid_root_route(self):
        response = self.app.get("/", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"api server: Authentication required for use", response.data)

    def test_invalid_route(self):
        response = self.app.get("/aaa", follow_redirects=True)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"Not Found:", response.data)

    def test_missing_authentication(self):
        response = self.app.get("/rastrea2r/api/v1.0/echo", follow_redirects=True)
        self.assertEqual(response.status_code, 401)
        self.assertIn(b"Authentication Failed:", response.data)

    def test_basic_authentication(self):
        headers = {
            "Authorization": "Basic %s"
            % b64encode(b"testuser:testpasswd").decode("ascii")
        }
        response = self.app.get(
            "/rastrea2r/api/v1.0/echo?message=test", headers=headers
        )
        self.assertIn(b"test", response.data)
        self.assertEqual(response.status_code, 200)

    def test_invalid_authentication(self):
        headers = {
            "Authorization": "Basic %s" % b64encode(b"invalid:invalid").decode("ascii")
        }
        response = self.app.get(
            "/rastrea2r/api/v1.0/echo?message=test", headers=headers
        )
        self.assertIn(b"Authentication Failed", response.data)
        self.assertEqual(response.status_code, 401)

    def test_method_not_allowed(self):
        headers = {
            "Authorization": "Basic %s"
            % b64encode(b"testuser:testpasswd").decode("ascii")
        }
        response = self.app.delete(
            "/rastrea2r/api/v1.0/echo?message=test", headers=headers
        )
        self.assertIn(b"Method Not Allowed", response.data)
        self.assertEqual(response.status_code, 405)

    def test_missing_attribute(self):
        headers = {
            "Authorization": "Basic %s"
            % b64encode(b"testuser:testpasswd").decode("ascii")
        }
        response = self.app.get("/rastrea2r/api/v1.0/echo", headers=headers)
        self.assertIn(b"Must provide message attribute via GET", response.data)
        self.assertEqual(response.status_code, 200)

    def test_valid_info(self):
        headers = {
            "Authorization": "Basic %s"
            % b64encode(b"testuser:testpasswd").decode("ascii")
        }
        response = self.app.get("/rastrea2r/api/v1.0/info", headers=headers)
        self.assertIn(b"Flask API Data", response.data)
        self.assertEqual(response.status_code, 200)

    def test_valid_key_info(self):
        headers = {
            "Authorization": "Basic %s"
            % b64encode(b"testuser:testpasswd").decode("ascii")
        }
        response = self.app.get(
            "/rastrea2r/api/v1.0/info?key=remoteaddr", headers=headers
        )
        self.assertIn(b"GET", response.data)
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
