#!/bin/bash

export ENV_FOLDER_NAME=env
export PYTHON_PATH=/usr/bin/python3

#Create ENV for python
if [ -d ${ENV_FOLDER_NAME} ];
then
    echo "Directory ${ENV_FOLDER_NAME} already exists"
else
    virtualenv ${ENV_FOLDER_NAME} --python=${PYTHON_PATH}
fi

echo "env directory is build"