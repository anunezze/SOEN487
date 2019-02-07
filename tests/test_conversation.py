import unittest
import json
from main import app as tested_app
from main import db as tested_db
from config import TestConfig
from models import Conversation, Message

tested_app.config.from_object(TestConfig)


class TestConversation(unittest.TestCase):
    def setUp(self):
        self.db = tested_db
        self.db.create_all()
        self.db.session.add(Conversation(creator_id=1, participant_id=3))
        self.db.session.add(Conversation(creator_id=2, participant_id=4))
        self.db.session.add(Message(conversation_id=1, sender_id=1, text="test1"))
        self.db.session.add(Message(conversation_id=1, sender_id=1, text="test2"))

        self.db.session.commit()

        self.app = tested_app.test_client()

    def tearDown(self):
        # clean up the DB after the tests
        Conversation.query.delete()
        Message.query.delete()
        self.db.session.commit()

    def test_get_all_conversations(self):
        response = self.app.get("/conversation")
        self.assertEqual(response.status_code, 200)

        conversations = json.loads(str(response.data, "utf8"))
        self.assertEqual(type(conversations), list)
        self.assertDictEqual(conversations[0], {"creator_id": "1", "participant_id": "3", "id":"1"})
        self.assertDictEqual(conversations[1], {"creator_id": "2", "participant_id": "4", "id": "2"})

    def test_post_conversation(self):
        initial_count = Conversation.query.filter_by(creator_id=3).count()

        response = self.app.post("/conversation", json={"creator_id": "3", "participant_id": "1"})
        print(response.status_code)
        self.assertEqual(response.status_code, 201)

        updated_count = Conversation.query.filter_by(creator_id=3).count()
        self.assertEqual(updated_count, initial_count + 1)

    def test_get_conversation(self):
        response = self.app.get("/conversation/1")
        self.assertEqual(response.status_code, 200)

        conversations = json.loads(str(response.data, "utf8"))
        self.assertDictEqual(conversations, {"id": 1, "creator_id": 1, "messages": [], "participant_id": 3})

    def test_get_conversation_with_message_limit(self):
        response = self.app.get("/conversation/1/1")
        self.assertEqual(response.status_code, 200)

        conversation = json.loads(str(response.data, "utf8"))
        self.assertEqual(conversation['id'], 1)
        self.assertEqual(conversation['creator_id'], 1)
        self.assertEqual(conversation['participant_id'], 3)
        self.assertEqual(conversation['messages'][0]['conversation_id'],"1")
        self.assertEqual(conversation['messages'][0]['id'], "2")
        self.assertEqual(conversation['messages'][0]['sender_id'], "1")
        self.assertEqual(conversation['messages'][0]['text'], "test2")


if __name__ == '__main__':
    unittest.main()
