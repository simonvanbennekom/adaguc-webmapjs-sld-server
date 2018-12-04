# File: Server.py

from flask import Flask, request
import configparser
import sys
import os
import glob
import xml.etree.ElementTree as ET

app = Flask(__name__)

#Load config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

@app.route('/processSLD', methods=['POST'])
@app.route('/processSLD/<fileName>', methods=['POST'])
def processSLD(fileName = '') :
    if not request.data :
        return 'SLD file cannot be empty'
    else : 
        if isValidFileSize(request.data) :
            #read SLD data into string
            requestData = ''.join(map(chr, request.data))
            
            # starts with <?xml> and ends with StyledLayerDescriptor>
            if(requestData.startswith('<?xml') == False or requestData.endswith('StyledLayerDescriptor>') == False) :
                return 'Invalid SLD, not matching standard'
                
            #Parse XML and catch error if raised
            try:
                tree = ET.ElementTree(ET.fromstring(requestData))
            except ET.ParseError as error:
                row, column = error.position
                return 'Invalid XML on line number: %i' % row
                        
            #Have FileName
            if fileName :
                if fileNameExists(fileName) : 
                    return 'Your file name:  %s.xml already exists. Try another' % fileName
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
                    fileUploadPath = os.path.join(config.get('SLD', 'DIR'), fileName + '.xml')
                    file = open(fileUploadPath, "w")
                    file.write(requestData)

                    #TODO return SLD URL
                    url = os.path.realpath(file.name)
                    file.close()

                    return url                    
                else :
                    return 'Filename must contain at least 4 characters'
            else : 
                return 'Something went wrong generating a fileName, try to submit again...'            
        else : 
            return 'File size to big'


#Check if file size is not greater then the MaxFileSize
def isValidFileSize(file = '') :
    return sys.getsizeof(file) <= config.getint('SLD', 'MaxFileSize')

def generateFileName(numberToAppend, defaultFilesNames) :
    #Create fileName
    uniqueFileName = config.get('SLD', 'DefaultFileName') + '_' + str(numberToAppend)
    print(uniqueFileName)
    
    if uniqueFileName in defaultFilesNames :
        generateFileName(numberToAppend+1, defaultFilesNames)
    
    return uniqueFileName

def fileNameExists(fileName) :
    uniqueFileName = config.get('SLD', 'DefaultFileName')
    return fileName in getAllFileNames()

#Get fileNames from dir where sldFiles are stored. 
def getAllFileNames(filter = '*.xml') :
    path = config.get('SLD', 'DIR') + filter
    return [os.path.splitext(os.path.basename(x))[0] for x in glob.glob(path)]
