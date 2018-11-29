# File: Server.py

from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/processSLD/<file>', methods=['POST'])
def processSLD(file) :
    def catch_all(file):
        request_data = request.get_data()
        if not request_data :
            return 'No SLD '
        else :
            app.logger.debug('Body: %s', request_data)
            return 'File argument: %s' % file
    return "hallo"
