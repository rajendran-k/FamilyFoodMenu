from flask import Flask, jsonify, request
import json
from flask_pymongo import PyMongo
from jinja2 import debug

import business.server as server
import business.menu as menu

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://db:27017/foodmenu'
mongo = PyMongo(app)

@app.route('/status')
def getStatusCheck():
    return server.getStatusCheck(request)

@app.route('/getmenu')
def getMenu():
    return menu.getMenu(mongo)

@app.route('/work')
def getWork():
    con =mongo.db.hel
    jj = {
            'name': "a",
            'description': "b"
    }
    try:
        id = con.insert_one(jj)
    except Exception as e:
        print("An exception occurred ::", e)
    return jsonify("Added "),200

@app.route('/addmenu', methods=['POST'])
def addMenu():
    return menu.addMenu(mongo,request)


@app.route('/addmenu', methods=['PUT'])
def updateMenu():
    return menu.updateMenu(mongo,request)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug = True)