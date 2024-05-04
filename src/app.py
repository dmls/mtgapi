#!flask/bin/python
from flask import Flask
from bson import json_util
import json

from db_manager import DBManager

def jsonify(bson = None):
    return json.loads(json_util.dumps(bson))


app = Flask(__name__)
dbm = DBManager()

@app.route('/mtgapi/v1.0/cards', methods = ['GET'])
def get_cards():
    col = dbm.db['cards']
    return jsonify(col.find_one())

if __name__ == '__main__':
    app.run(debug = True)
