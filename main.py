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


# @app.route("/person/<person_id>")
# def get_person(person_id):
#     # id is a primary key, so we'll have max 1 result row
#     person = Person.query.filter_by(id=person_id).first()
#     if person:
#         return jsonify(row2dict(person))
#     else:
#         return make_response(jsonify({"code": 404, "msg": "Cannot find this person id."}), 404)


# @app.route("/person", methods={"PUT"})
# def put_person():
#     # get the name first, if no name then fail
#     name = request.form.get("name")
#     if not name:
#         return make_response(jsonify({"code": 403,
#                                       "msg": "Cannot put person. Missing mandatory fields."}), 403)
#     person_id = request.form.get("id")
#     if not person_id:
#         p = Person(name=name)
#     else:
#         p = Person(id=person_id, name=name)
#
#     db.session.add(p)
#     try:
#         db.session.commit()
#     except sqlalchemy.exc.SQLAlchemyError as e:
#         error = "Cannot put person. "
#         print(app.config.get("DEBUG"))
#         if app.config.get("DEBUG"):
#             error += str(e)
#         return make_response(jsonify({"code": 404, "msg": error}), 404)
#     return jsonify({"code": 200, "msg": "success"})


if __name__ == '__main__':
    app.run()
