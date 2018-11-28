# File: Server.py

from flask import Flask
from flask import request

app = Flask(__name__)

@app.route('/processSLD', methods=['POST'])
def proccessSLD():
    return 'Hello, World!'