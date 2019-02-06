from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = r"sqlite:///soen487a1.sqlite"
db = SQLAlchemy(app)

## Copy Models from models.py


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.Text(), nullable=False, unique=True)
    createdConvo = db.relationship("Conversation", backref="creator", lazy="dynamic", foreign_keys="Conversation.creator_id")
    participantConvo = db.relationship("Conversation", backref="participant", lazy="dynamic" ,foreign_keys="Conversation.participant_id")
    messages_sent = db.relationship("Message")
    # def __repr__(self):
    #     return "<User {}: {}>".format(self.id, self.username)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    participant_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    messages = db.relationship("Message", backref="messages")


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    creation_time = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    text = db.Column(db.Text(), nullable=False)
