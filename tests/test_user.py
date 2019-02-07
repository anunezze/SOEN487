import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import User

tested_app.config.from_object(TestConfig)


class TestUser(unittest.TestCase):
    def setUp(self):
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(User(username="andres"))
        self.db.session.add(User(username="marcos"))
        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        User.query.delete()
        self.db.session.commit()

    def test_get_all_user(self):
        response = self.app.get("/user")
        self.assertEqual(response.status_code, 200)

        user_list = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(user_list), list)
        self.assertDictEqual(user_list[0], {"id": "1", "name": "andres"})
        self.assertDictEqual(user_list[1], {"id": "2", "name": "marcos"})


if __name__ == '__main__':
    unittest.main()
