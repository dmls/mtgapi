#!flask/bin/python
from bson import json_util
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from functools import wraps
import json
import os

from db_manager import DBManager
from user import User

load_dotenv()

def bson_jsonify(bson = None):
    return json.loads(json_util.dumps(bson))


app = Flask(__name__)
dbm = DBManager()


@app.route('/mtgapi/v1.0/auth/login', methods = ['POST'])
def login():
    data = request.json
    print(data)
    user = User(dbm)
    token = user.gen_auth_token(
        data.get('email'),
        data.get('password')
    )

    if not token:
        return {'message': 'Invalid credentials'}, 401

    return {'token': token}, 200

def validate_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        invalid_msg = jsonify({
            'message': 'Missing or invalid authentication token.'
        }), 401

        token = request.headers.get('Authorization')
        if not token:
            return invalid_msg

        user = User(dbm)
        if not user.validate_auth_token(token):
            return invalid_msg

        return func(*args, **kwargs)

    return wrapper

@app.route('/mtgapi/v1.0/cards', methods = ['GET'])
@validate_token
def get_cards():
    col = dbm.db['cards']
    return bson_jsonify(col.find_one())

if __name__ == '__main__':
    app.run(debug = True)
