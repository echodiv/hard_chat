from app import db, create_app
from app.models import Users, Posts, Messages
from config import TestConfig
from datetime import datetime, timedelta
import unittest
import random
import json


class UsersModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = Users(name='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_follow(self):
        u1 = Users(name='john', email='john@example.com')
        u2 = Users(name='susan', email='susan@example.com')
        db.session.add_all([u1, u2])
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().name, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().name, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = Users(name='john', email='john@example.com')
        u2 = Users(name='susan', email='susan@example.com')
        u3 = Users(name='mary', email='mary@example.com')
        u4 = Users(name='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Posts(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Posts(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Posts(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Posts(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])

    @unittest.skip("function is not supported")
    def test_user_posts_in_json(self):
        user = Users(name='Name', email='name@example.com')
        db.session.add(user)

        # create four posts
        now = datetime.utcnow()
        for i in range(10):
            post = Posts(body="post_{}".format(i), 
                         author=user,
                         timestamp=now + timedelta(seconds=i))
            db.session.add(post)


class PostsModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        user = Users(name='Marcus', sename='Antoninus', email='test@gmail.net')
        db.session.add(user)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_publish_post(self):
        user = Users.query.filter_by(email='test@gmail.net').first_or_404()
        now = datetime.utcnow()
        post = Posts(body="post content", author=user)
        db.session.add(post)
        db.session.commit()
        selected_post = Posts.query.first()
        all_selected_post = Posts.query.all()

        check_post = {"post_id": 1, 
                      "post_body": "post content", 
                      "timestamp": str(selected_post.timestamp), 
                      "author_id": 1}

        selected_post = json.loads(str(selected_post))

        self.assertEqual(len(all_selected_post), 1)
        self.assertEqual(selected_post['author_id'], check_post['author_id'])
        self.assertEqual(selected_post['post_body'], check_post['post_body'])
        self.assertEqual(selected_post['post_id'], check_post['post_id'])
        self.assertEqual(len(selected_post.keys()), 4)
        self.assertEqual(check_post.keys(), selected_post.keys())


class MessagesModelCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        u1 = Users(name='Marcus', sename='Antoninus', email='test_1@gmail.net')
        u2 = Users(name='Lucius', sename='Vorenus', email='test_2@gmail.net')
        u3 = Users(name='Julius', sename='Caesar', email='test_3@gmail.net')
        db.session.add_all([u1, u2, u3])

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_send_message(self):
        user_1 = Users.query.filter_by(email='test_1@gmail.net').first_or_404()
        user_2 = Users.query.filter_by(email='test_2@gmail.net').first_or_404()
        msg1 = Messages(author=user_1, recipient=user_2, body='message_1')
        msg2 = Messages(author=user_2, recipient=user_1, body='message_2')
        msg3 = Messages(author=user_1, recipient=user_2, body='message_3')
        db.session.add_all([msg1, msg2, msg3])
        msg_from_u1 = Messages.query.filter_by(author=user_1).all()
        msg_from_u2 = Messages.query.filter_by(author=user_2).all()

        self.assertEqual(len(msg_from_u1), 2)
        self.assertEqual(len(msg_from_u2), 1)
