#!flask/bin/python
from bson import json_util
from dotenv import load_dotenv
from flask import Flask, request
import json
import os

from db_manager import DBManager
from user import User

load_dotenv()

def jsonify(bson = None):
    return json.loads(json_util.dumps(bson))


app = Flask(__name__)
dbm = DBManager()

@app.route('/mtgapi/v1.0/cards', methods = ['GET'])
def get_cards():
    col = dbm.db['cards']
    return jsonify(col.find_one())


@app.route('/mtgapi/v1.0/auth/login', methods = ['POST'])
def login():
    user = User(dbm)
    token = user.gen_auth_token(
        request.args.get('email'),
        request.args.get('password')
    )

    if not token:
        return {'message': 'Invalid credentials'}, 401

    return {'token': token}, 200

if __name__ == '__main__':
    app.run(debug = True)
