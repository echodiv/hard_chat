from app import db, login
from flask import current_app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.search import add_to_index, remove_from_index, query_index
from time import time
import jwt


followers = db.Table('followers',
        db.Column('follower_id', db.Integer, db.ForeignKey('users.id')),
        db.Column('followed_id', db.Integer, db.ForeignKey('users.id')))


class SearchableMixin(object):
    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = []
        for i in range(len(ids)):
            when.append((ids[i], i))
        return cls.query.filter(cls.id.in_(ids)).order_by(
            db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            'add': list(session.new),
            'update': list(session.dirty),
            'delete': list(session.deleted)
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes['add']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['update']:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes['delete']:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


class Users(UserMixin, db.Model):
    __tablename__ = 'users'

    def set_password(self, row_pwd):
        self.password = generate_password_hash(row_pwd)

    def check_password(self, row_pwd):
        return check_password_hash(self.password, row_pwd)

    id = db.Column(db.Integer, 
            primary_key=True)
    reg_time = db.Column(db.DateTime, 
            index=True, 
            default=datetime.utcnow)
    last_visit_time = db.Column(db.DateTime, 
            index=True, 
            default=datetime.utcnow)
    name = db.Column(db.String(64))
    sename = db.Column(db.String(64))
    email = db.Column(db.String(128), 
            index=True, 
            unique=True)
    password = db.Column(db.String(128))
    phone = db.Column(db.String(12))
    status = db.Column(db.Integer)
    text_status = db.Column(db.String(256))
    followed = db.relationship('Users', secondary=followers,
            primaryjoin=(followers.c.follower_id == id),
            secondaryjoin=(followers.c.followed_id == id),
            backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')
    posts = db.relationship('Posts', backref='author', lazy='dynamic')

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
            followers, (followers.c.followed_id == Posts.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Posts.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Posts.timestamp.desc())

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return Users.query.get(id)

    def __repr__(self):
        return f'<User {self.name} with id {self.id} and email {self.email}>\n'

class Posts(SearchableMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    __searchable__ = ['body']

    def __repr__(self):
        return '<Post {}>'.format(self.body)

class Chats(db.Model):
    __tablename__ = 'chats'

    id = db.Column(db.Integer, 
            primary_key=True)
    create_time = db.Column(db.DateTime, 
            index=True, 
            default=datetime.utcnow)
    name = db.Column(db.String(128))
    status = db.Column(db.Integer)
    description = db.Column(db.String(128))

    def __repr__(self):
        return f'Chat id {self.id} with name {name}\n'


class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, 
            primary_key=True)
    send_time = db.Column(db.DateTime, 
            index=True, 
            default=datetime.utcnow)
    message = db.Column(db.Text(512))
    type = db.Column(db.Integer)
    status = db.Column(db.Integer)
    uid = db.Column(db.Integer, 
            db.ForeignKey('users.id'))
    chat_id = db.Column(db.Integer, 
            db.ForeignKey('chats.id'))

    def __repr__(self):
        return f'Message id {id} from user with id {uid}\n'


class Talkers(db.Model):
    __tablename__ = 'talkers'

    user_role = db.Column(db.Integer,
            primary_key=False)
    status = db.Column(db.Integer,
            primary_key=False)
    uid = db.Column(db.Integer, 
            db.ForeignKey('users.id'),
            primary_key=True)
    chat_id = db.Column(db.Integer, 
            db.ForeignKey('chats.id'),
            primary_key=False)

    def __repr__(self):
        return f'{self.uid} talk in chat {self.chat_id}'


@login.user_loader
def load_user(id: int) -> Users:
    return Users.query.get(int(id))

db.event.listen(db.session, 'before_commit', SearchableMixin.before_commit)
db.event.listen(db.session, 'after_commit', SearchableMixin.after_commit)
