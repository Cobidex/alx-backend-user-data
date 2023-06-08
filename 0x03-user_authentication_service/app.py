#!/usr/bin/env python3
""" sets up a flask app """
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

AUTH = Auth()
app = Flask(__name__)


@app.route('/', strict_slashes=False)
def default():
    """ default route """
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def POST_user():
    """ registers a new user """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email=email, password=password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """ logs in a user """
    email = request.form.get('email')
    password = request.form.get('password')

    if not AUTH.valid_login(email=email, password=password):
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response({"email": email, "message": "logged in"})
    response.set_cookie('session_id', session_id)
    return response


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout():
    """ logs out a user """
    session_id = request.cookies("session_id")
    try:
        user = AUTH.get_user_from_session_id(session_id)
        AUTH.destroy_session(user.id)
        redirect("/")
    except NoResultFound:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
