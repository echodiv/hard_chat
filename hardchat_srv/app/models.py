import json
from datetime import datetime
from time import time

import jwt
from app import db, login
from app.search import add_to_index, query_index, remove_from_index
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

followers = db.Table(
    "followers",
    db.Column("follower_id", db.Integer, db.ForeignKey("users.id")),
    db.Column("followed_id", db.Integer, db.ForeignKey("users.id")),
)


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            "items": [item.to_dict() for item in resources.items],
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total_pages": resources.pages,
                "total_items": resources.total,
            },
        }
        return data


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return (
            cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)),
            total,
        )

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted),
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes["add"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["update"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)


class Messages(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    recipient_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return "<Message {}>".format(self.body)


class Users(UserMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = "users"

    def set_password(self, row_pwd):
        if len(row_pwd) < 8:
            raise Exception(
                f"Password too short. Got {len(row_pwd)} symbols, "
                "expected password must be longer than 7"
            )
        self.password = generate_password_hash(row_pwd)

    def check_password(self, row_pwd):
        if len(row_pwd) < 8:
            raise Exception(
                f"Password too short. Get {len(row_pwd)} symbols",
                "expected password must be longer than 7",
            )
        return check_password_hash(self.password, row_pwd)

    id = db.Column(db.Integer, primary_key=True)
    reg_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    last_visit_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    name = db.Column(db.String(64))
    sename = db.Column(db.String(64))
    email = db.Column(db.String(128), index=True, unique=True)
    password = db.Column(db.String(128))
    phone = db.Column(db.String(12))
    status = db.Column(db.Integer)
    text_status = db.Column(db.String(256))
    followed = db.relationship(
        "Users",
        secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref("followers", lazy="dynamic"),
        lazy="dynamic",
    )
    posts = db.relationship("Posts", backref="author", lazy="dynamic")
    messages_sent = db.relationship(
        "Messages", foreign_keys="Messages.sender_id", backref="author", lazy="dynamic"
    )
    messages_received = db.relationship(
        "Messages",
        foreign_keys="Messages.recipient_id",
        backref="recipient",
        lazy="dynamic",
    )
    last_message_read_time = db.Column(db.DateTime)

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        followed = Posts.query.join(
            followers, (followers.c.followed_id == Posts.user_id)
        ).filter(followers.c.follower_id == self.id)
        own = Posts.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Posts.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        ).decode("utf-8")

    def new_messages(self):
        last_read_time = self.last_message_read_time or datetime(1900, 1, 1)
        return (
            Messages.query.filter_by(recipient=self)
            .filter(Messages.timestamp > last_read_time)
            .count()
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except Exception:
            return
        return Users.query.get(id)

    def __repr__(self):
        return f"<User {self.name} with id {self.id} and email {self.email}>\n"


class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    timestamp = db.Column(db.Float, index=True, default=time)
    payload_json = db.Column(db.Text)

    def get_data(self):
        return json.loads(str(self.payload_json))


class Posts(SearchableMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    __searchable__ = ["body"]

    def to_dict(self):
        """Return posts in dict format"""
        try:
            user = Users.query.filter_by(id=self.user_id).first()
        except Exception:
            # toDo: read exception ond fix it (unittests)
            return {"error": "500", "reason": "error with key sql_1"}

        data = {
            "id": self.id,
            "post_content": self.body,
            "post_time": self.timestamp.isoformat() + "Z",
            "author": {
                "id": self.user_id,
                "name": user.name,
                "sename": user.sename,
            },
        }
        return data

    def from_dict(self, data):
        for field in ["id", "body", "timestamp", "user_id"]:
            if field in data:
                setattr(self, field, data[field])

    def __repr__(self):
        resp = {
            "post_id": self.id,
            "post_body": self.body,
            "timestamp": str(self.timestamp),
            "author_id": self.user_id,
        }
        return str(json.dumps(resp))


@login.user_loader
def load_user(id: int) -> Users:
    return Users.query.get(int(id))
