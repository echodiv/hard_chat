import json
import unittest

from app import create_app, db
from app.models import Posts, Users
from config import TestConfig


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
        post = Posts(body="post content", author=user)
        db.session.add(post)
        db.session.commit()
        selected_post = Posts.query.first()

        check_post = {
            "post_id": 1,
            "post_body": "post content",
            "timestamp": str(selected_post.timestamp),
            "author_id": 1
        }

        selected_post = json.loads(str(selected_post))

        self.assertEqual(selected_post['author_id'], check_post['author_id'])
        self.assertEqual(selected_post['post_body'], check_post['post_body'])
        self.assertEqual(selected_post['post_id'], check_post['post_id'])
        self.assertEqual(len(selected_post.keys()), 4)
        self.assertEqual(check_post.keys(), selected_post.keys())

    def test_add_just_one_post(self):
        user = Users.query.filter_by(email='test@gmail.net').first_or_404()
        post = Posts(body="post content", author=user)
        db.session.add(post)
        db.session.commit()
        all_selected_post = Posts.query.all()
        self.assertEqual(len(all_selected_post), 1)
