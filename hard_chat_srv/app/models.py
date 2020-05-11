from app import db
from datetime import datetime


class Users(db.Model):
    __tablename__ = 'users'

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

    def __repr__(self):
        return f'<User {self.name} with id {self.id} and email {self.email}>\n'


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

