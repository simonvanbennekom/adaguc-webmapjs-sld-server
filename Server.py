# File: Server.py

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

import configparser
import sys
import os
import glob
import xml.etree.ElementTree as ET

app = Flask(__name__)
CORS(app)

#Load config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

#Retrieve SLD files from sldFiles folder
@app.route('/' + config.get('SLD', 'DIR') + '<path>', methods=['GET'])
def send_js(path):
    return send_from_directory(config.get('SLD', 'DIR'), path)

@app.route('/processSLD', methods=['POST'])
@app.route('/processSLD/<fileName>', methods=['POST'])
def processSLD(fileName = '') :
    if not request.get_data() :
        return createErrorResponse('SLD file cannot be empty')
    else :
        if isValidFileSize(request.get_data()) :
            #read SLD data into string
            requestData = ''.join(map(chr, request.get_data()))
            
            # starts with <?xml> and ends with StyledLayerDescriptor>
            if(requestData.startswith('<?xml') == False or requestData.endswith('StyledLayerDescriptor>') == False) :
                return createErrorResponse('Invalid SLD, not matching standard')
                
            #Parse XML and catch error if raised
            try:
                tree = ET.ElementTree(ET.fromstring(requestData))
            except ET.ParseError as error:
                row, column = error.position
                return createErrorResponse('Invalid XML on line number: %i' % row)

            #Have FileName
            if fileName :
                if fileNameExists(fileName) : 
                    return createErrorResponse('Your file name:  %s.xml already exists. Try another' % fileName)
            else :
                #Generate a filename

                #Check defaultFileNames
                filter = config.get('SLD', 'DefaultFileName') + '*.xml'
                defaultFileNames = getAllFileNames(filter)

                #Count amount of files
                numberToAppend = len(defaultFileNames)
                fileName = generateFileName(numberToAppend+1, defaultFileNames)           

            #Double check if fileName still exists
            if fileName :
                #Check if fileName contain at least 4 characters
                if len(fileName) >= 4 :
                    fileUploadPath = os.path.join(config.get('SLD', 'DIR'), getFileNameWithExtension(fileName))
                    file = open(fileUploadPath, "w")
                    file.write(requestData)
                    file.close()

                    return createSuccessResponse('SLD is succesfully created!', {'url' : request.host_url + config.get('SLD', 'DIR') + getFileNameWithExtension(fileName) })
                else :
                    return createErrorResponse('Filename must contain at least 4 characters')
            else : 
                return createErrorResponse('Something went wrong generating a fileName, try to submit again...')
        else : 
            return createErrorResponse('File size to big')


#Check if file size is not greater then the MaxFileSize
def isValidFileSize(file = '') :
    return sys.getsizeof(file) <= config.getint('SLD', 'MaxFileSize')

def generateFileName(numberToAppend, defaultFilesNames) :
    #Create fileName
    uniqueFileName = config.get('SLD', 'DefaultFileName') + '_' + str(numberToAppend)
    
    if uniqueFileName in defaultFilesNames :
        generateFileName(numberToAppend+1, defaultFilesNames)
    
    return uniqueFileName

def fileNameExists(fileName) :
    uniqueFileName = config.get('SLD', 'DefaultFileName')
    return fileName in getAllFileNames()

#Get fileNames from dir where sldFiles are stored. 
def getAllFileNames(filter = '*.xml') :
    path = './' + config.get('SLD', 'DIR') + filter
    return [os.path.splitext(os.path.basename(x))[0] for x in glob.glob(path)]

def createErrorResponse(message, data = None) :
    return createResponse('error', message, data)

def createSuccessResponse(message, data = None) :
    return createResponse('success', message, data)    

def createResponse(status,message, data = None) :
    return jsonify(status=status,message=message,data=data)

def getFileNameWithExtension(fileName) :
    return fileName + '.xml'
