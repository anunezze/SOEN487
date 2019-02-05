from flask_sqlalchemy import SQLAlchemy
from main import app

db = SQLAlchemy(app)

def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text(), nullable=False, unique=True)
    createdConvo = db.relationship("Conversation", backref="creator", lazy="dynamic", foreign_keys="Conversation.creator_id")
    participantConvo = db.relationship("Conversation", backref="participant", lazy="dynamic" ,foreign_keys="Conversation.participant_id")
    messages_sent = db.relationship("Message")
    # def __repr__(self):
    #     return "<User {}: {}>".format(self.id, self.username)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    participant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages = db.relationship("Message", backref="messages")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # creation_time = db.Column(DateTime)
    text = db.Column(db.Text(), nullable=False)
