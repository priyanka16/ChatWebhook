from flask import Flask, request, jsonify, redirect, abort, make_response
from datetime import datetime,date,timedelta
from dateutil import relativedelta
from collections import OrderedDict
from random import randint
import json

app = Flask(__name__)

@app.route("/")
def homepage():
    return "This is just the start of the world"

if __name__ == '__main__':
    app.run()
