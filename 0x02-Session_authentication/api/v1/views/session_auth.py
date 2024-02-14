#!/usr/bin/env python3
"""handles all routes for the Session authentication."""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """login method"""
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None:
        return jsonify({"error": "email missing"}), 400
    if password is None:
        return jsonify({"error": "password missing"}), 400
    user_email = User.search({'email': email})
    if not user_email:
        return jsonify({"error": "no user found for this email"}), 404
    if not user_email[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user_email[0].id)
    out = jsonify(user_email[0].to_json())
    out.set_cookie(os.getenv('SESSION_NAME'), session_id)
    return out
