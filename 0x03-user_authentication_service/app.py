#!/usr/bin/env python3
'''flask app'''
from flask import (Flask, jsonify, request, abort, make_response, redirect,
                   url_for)
from auth import Auth
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound

AUTH = Auth()

app = Flask(__name__)


@app.route('/', strict_slashes=False, methods=['GET'])
def index():
    '''index of the flask app'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', strict_slashes=False, methods=['POST'])
def user() -> str:
    '''creating user'''
    email = request.args.get('email')
    password = request.args.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({f"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', strict_slashes=False, methods=['POST'])
def login():
    '''login function'''
    email = request.args.get('email')
    password = request.args.get('password')
    user = AUTH.valid_login(email, password)
    if not user:
        abort(401)
    session_id = AUTH.create_session(email)
    res = jsonify({"email": email, "message": "logged in"})
    res = make_response(res)
    res.set_cookie('session_id', session_id)
    return res


@app.route('/sessions', strict_slashes=False, methods=['DELETE'])
def logout():
    '''logout function'''
    cookie = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(cookie)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', strict_slashes=False, methods=['GET'])
def profile():
    '''finds user email'''
    cookie = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(cookie)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route('/reset_password', strict_slashes=False, methods=['POST'])
def get_reset_password_token():
    '''reset password token'''
    email = request.args.get('email')
    try:
        user = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": user})


@app.route('/reset_password', strict_slashes=False, methods=['PUT'])
def update_password():
    '''update password'''
    email = request.args.get('email')
    password = request.args.get('new_password')
    reset_token = request.args.get('reset_token')
    try:
        user = AUTH.update_password(reset_token, password)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "message": "Password updated"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
