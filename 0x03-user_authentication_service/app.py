#!/usr/bin/env python3
""" sets up a flask app """
from flask import Flask, jsonify, request, abort, make_response
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")