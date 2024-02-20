#!/usr/bin/env python3
'''flask app'''
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route('/', strict_slashes=False, methods=['GET'])
def index():
    '''index of the flask app'''
    form = request.form.get('message')
    return jsonify(form)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
