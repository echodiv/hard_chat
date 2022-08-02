import unittest
from datetime import datetime, timedelta

from app import create_app, db
from app.models import Posts, Users
from config import TestConfig


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

    def test_password_length_is_7_too_short(self):
        u = Users(name="John")
        self.assertRaises(Exception, u.set_password, "1234567")

    def test_set_good_password_with_len_8_and_check_it(self):
        u = Users(name="John")
        u.set_password("1234567a")
        db.session.commit()
        self.assertTrue(u.check_password("1234567a"))

    def test_new_user_do_not_follow_anyone(self):
        u1 = Users(name="john", email="john@example.com")
        u2 = Users(name="susan", email="susan@example.com")
        db.session.add_all([u1, u2])
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])

    def test_follow_user(self):
        u1 = Users(name="john", email="john@example.com")
        u2 = Users(name="susan", email="susan@example.com")
        db.session.add_all([u1, u2])
        db.session.commit()
        u1.follow(u2)
        self.assertTrue(u1.is_following(u2))

    def test_unfollow_user(self):
        u1 = Users(name="john", email="john@example.com")
        u2 = Users(name="susan", email="susan@example.com")
        db.session.add_all([u1, u2])
        db.session.commit()

        u1.follow(u2)
        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))

    def test_follow_posts(self):
        # create four users
        u1 = Users(name="john", email="john@example.com")
        u2 = Users(name="susan", email="susan@example.com")
        db.session.add_all([u1, u2])
        now = datetime.utcnow()
        p1 = Posts(
            body="post from john",
            author=u1,
            timestamp=now + timedelta(seconds=1),
        )
        p2 = Posts(
            body="post from susan",
            author=u2,
            timestamp=now + timedelta(seconds=4),
        )
        db.session.add_all([p1, p2])
        u1.follow(u2)
        db.session.commit()
        f1 = u1.followed_posts().all()
        self.assertEqual(f1, [p2, p1])

    def test_is_following_user(self):
        u1 = Users(name="john", email="john@example.com")
        u2 = Users(name="susan", email="susan@example.com")
        db.session.add_all([u1, u2])
        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))

    def unfollow_user_and_check_is_following(self):
        u1 = Users(name="john", email="john@example.com")
        u2 = Users(name="susan", email="susan@example.com")
        db.session.add_all([u1, u2])
        u1.follow(u2)
        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))

    @unittest.skip("function is not supported")
    def test_user_posts_in_json(self):
        user = Users(name="Name", email="name@example.com")
        db.session.add(user)

        # create four posts
        now = datetime.utcnow()
        for i in range(10):
            post = Posts(
                body="post_{}".format(i),
                author=user,
                timestamp=now + timedelta(seconds=i),
            )
            db.session.add(post)
