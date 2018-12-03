# File: Server.py

from flask import Flask, jsonify, request
import configparser
import sys
import os
import glob
import xml.etree.ElementTree as ET

app = Flask(__name__)

#Load config.ini file
config = configparser.ConfigParser()
config.read("config.ini")

@app.route('/processSLD', methods=['POST'])
@app.route('/processSLD/<fileName>', methods=['POST'])
def processSLD(fileName = "") :
    if not request.data :
        return 'SLD file cannot be empty'
    else : 
        if isValidFileSize(request.data) :

            #read request data into string
            requestData = "".join(map(chr, request.data))
            
            # starts with <?xml> and ends with StyledLayerDescriptor>
            if(requestData.startswith("<?xml") == False or requestData.endswith("StyledLayerDescriptor>") == False) :
                return 'Invalid SLD, not matching standard'
                
            #Parse XML and catch error if raised
            try:
                tree = ET.ElementTree(ET.fromstring(requestData))
            except ET.ParseError as error:
                row, column = error.position
                return "Invalid XML on line number: %i" % row
            
            #Filename
            if not fileName :
                # path = config.get('SLD', 'Dir') . "/*.xml"
                # print(path)
                print(glob.glob("./sldFiles/*.xml"))
                print("Generate filename")
                
            #Have file name, check if exists


            # fileUploadPath = os.path.join('./sldFiles', 'sld.xml')
            # file = open(fileUploadPath, "w")  
            # file.write(requestData)
            # file.close()
            return 'File argument: %s' % fileName
            
        else : 
            return "File size to big"


#Check if file size is not greater then the MaxFileSize
def isValidFileSize(file = "") :
    return sys.getsizeof(file) <= config.getint('SLD', 'MaxFileSize')