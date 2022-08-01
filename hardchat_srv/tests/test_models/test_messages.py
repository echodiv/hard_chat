import unittest

from app import create_app, db
from app.models import Messages, Users
from config import TestConfig
from sqlalchemy.exc import IntegrityError


class MessagesModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        u1 = Users(name="Marcus", sename="Antoninus", email="test_1@gmail.net")
        u2 = Users(name="Lucius", sename="Vorenus", email="test_2@gmail.net")
        u3 = Users(name="Julius", sename="Caesar", email="test_3@gmail.net")
        db.session.add_all([u1, u2, u3])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_send_message(self):
        user_1 = Users.query.filter_by(email="test_1@gmail.net").first_or_404()
        user_2 = Users.query.filter_by(email="test_2@gmail.net").first_or_404()
        msg = Messages(author=user_1, recipient=user_2, body="message_1")

        db.session.add(msg)
        db.session.commit()
        get_msg = Messages.query.filter_by(author=user_1).all()

        self.assertEqual(len(get_msg), 1)

    def test_send_message_without_recipient(self):
        user_1 = Users.query.filter_by(email="test_1@gmail.net").first_or_404()
        msg = Messages(author=user_1, body="message_1")
        db.session.add(msg)
        with self.assertRaises(IntegrityError):
            db.session.commit()

    def test_send_message_without_author(self):
        user_1 = Users.query.filter_by(email="test_1@gmail.net").first_or_404()
        msg = Messages(recipient=user_1, body="message_1")
        db.session.add(msg)
        with self.assertRaises(IntegrityError):
            db.session.commit()
