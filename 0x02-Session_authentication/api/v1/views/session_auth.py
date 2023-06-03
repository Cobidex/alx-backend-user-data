#!/usr/bin/env python3
"""
views for session authentication routes
"""
from flask import request, jsonify, make_response
from api.v1.views import app_views
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', methods=['POST'],
                 strict_slashes=False)
def POST_login():
    email = request.form.get('email')
    password = request.form.get('password')

    if email is None:
        return jsonify({ "error": "email missing" }), 400

    if password is None:
        return jsonify({ "error": "password missing" }), 400
    
    users = User.search({'email': email})

    if len(users) == 0:
        return jsonify ({ "error": "no user found for this email" }), 404
    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session_id = auth.create_session(user.id)
            session_name = getenv('SESSION_NAME')
            response = make_response(user.to_json())
            response.set_cookie(session_name, session_id)
            return response
    return jsonify({ "error": "wrong password" }), 401
