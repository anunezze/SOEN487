from flask import Flask, jsonify, make_response, request
from config import DevConfig

import sqlalchemy

# need an app before we import models because models need it
app = Flask(__name__)
from models import db, row2dict, User, Conversation, Message

app.config.from_object(DevConfig)


@app.errorhandler(404)
def page_not_found(e):
    return make_response(jsonify({"code": 404, "msg": "404: Not Found"}), 404)


@app.route("/user", methods={"GET"})
def get_users():
    user_list = User.query.all();
    return jsonify([row2dict(person) for person in user_list])


@app.route("/user", methods={"POST"})
def post_user():
    username = request.get_json().get('username')
    if not username:
        return 'Please enter an username..'
    u = User(username=username)
    db.session.add(u)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put person. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)

    return make_response(jsonify({"id":u.id, "username":u.username}), 201)


@app.route("/conversation", methods={"GET"})
def get_conversations():
    conversation_list = Conversation.query.all()
    return jsonify([row2dict(conversation) for conversation in conversation_list])


@app.route("/conversation/<conversation_id>", methods={"GET"})
def get_messages(conversation_id):
    c = Conversation.query.filter_by(id=conversation_id).first()
    messages = Message.query.with_parent(c).order_by(Message.id.desc()).limit(3).all()
    response = jsonify({
        "id": c.id,
        "creator_id": c.creator_id,
        "participant_id": c.participant_id,
        "messages": [row2dict(m) for m in messages]
    })
    return make_response(response, 200)


@app.route("/conversation/<conversation_id>/<limit>", methods={"GET"})
def get_messages_with_limit(conversation_id, limit):
    c = Conversation.query.filter_by(id=conversation_id).first()
    messages = Message.query.with_parent(c).order_by(Message.id.desc()).limit(limit).all()
    response = jsonify({
        "id": c.id,
        "creator_id": c.creator_id,
        "participant_id": c.participant_id,
        "messages": [row2dict(m) for m in messages]
    })
    return make_response(response, 200)


@app.route("/conversation", methods={"POST"})
def create_conversation():
    creator_id = request.get_json().get("creator_id")
    participant_id = request.get_json().get("participant_id")
    if not creator_id or not participant_id:
        return "Missing a creator or an participant"
    c = Conversation(creator_id=creator_id,participant_id=participant_id)
    db.session.add(c)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put person. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return make_response(jsonify({
        "id": c.id,
        "creator_id": c.creator_id,
        "participant_id": c.participant_id
    }), 201)


@app.route("/message", methods={"POST"})
def post_message():
    conversation_id = request.get_json().get("conversation_id")
    sender_id = request.get_json().get("sender_id")
    text = request.get_json().get("text")
    if not conversation_id or not sender_id or not text:
        return "Missing body arguments"
    m = Message(conversation_id=conversation_id, sender_id=sender_id, text=text)
    db.session.add(m)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put person. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return make_response(jsonify({
        "id": m.id,
        "conversation_id": m.conversation_id,
        "sender_id": m.sender_id,
        "text": m.text
    }), 201)


@app.route("/message/<message_id>", methods={"DELETE"})
def delete_message(message_id):
    m = Message.query.filter_by(id=message_id).first()
    db.session.delete(m)
    try:
        db.session.commit()
    except sqlalchemy.exc.SQLAlchemyError as e:
        error = "Cannot put person. "
        print(app.config.get("DEBUG"))
        if app.config.get("DEBUG"):
            error += str(e)
        return make_response(jsonify({"code": 404, "msg": error}), 404)
    return make_response("Message was deleted", 202)


if __name__ == '__main__':
    app.run()
