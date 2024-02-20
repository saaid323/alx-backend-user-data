#!/usr/bin/env python3
'''flask app'''
from flask import Flask, jsonify, request
from auth import Auth

AUTH = Auth()

app = Flask(__name__)


@app.route('/', strict_slashes=False, methods=['GET'])
def index():
    '''index of the flask app'''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', strict_slashes=False, methods=['POST'])
def user():
    '''creating user'''
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
    except ValueError:
        return jsonify({"message": "email already registered"}), 400
    return jsonify({f"email": user.email, "message": "user created"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
