from flask_sqlalchemy import SQLAlchemy
from main import app

db = SQLAlchemy(app)


def row2dict(row):
    return {c.name: str(getattr(row, c.name)) for c in row.__table__.columns}


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text(), nullable=False)

    def __repr__(self):
        return "<User {}: {}>".format(self.id, self.username)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id1 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    user_id2 = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2 = db.relationship(User)


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    conversation_id = db.Column(db.Integer, db.ForeignKey('conversation.id'))
    conversation = db.relationship(Conversation)
    from_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship(User)
    # creation_time = db.Column(DateTime)
    text = db.Column(db.Text(), nullable=False)
