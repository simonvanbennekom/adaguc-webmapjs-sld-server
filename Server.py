# File: Server.py

from flask import Flask, jsonify, request
import sys
import os
import xml.etree.ElementTree as ET

app = Flask(__name__)

@app.route('/processSLD', methods=['POST'])
@app.route('/processSLD/<file_name>', methods=['POST'])
def processSLD(file_name = "") :
    request_data = "".join(map(chr, request.stream.read()))
    if not request_data :
        return 'No SLD is given'
    else :
        if not file_name :
            return 'No file_name is given'
        else :        
            #Check file
            ## > 10KB
            ## starts with <xml> and ends with </xml>
            ## Parse it and check if xml gives any errors

            tree = ET.ElementTree(ET.fromstring(request_data))
            tree.write("filename.xml")

            
            fileUploadPath = os.path.join('./sldFiles', 'sld.xml')
            file = open(fileUploadPath, "w")  
            file.write(request_data)
            file.close()
            return 'File argument: %s' % file_name
    return "hallo"

