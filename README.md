# adaguc-webmapjs-sld-server

REQ: Python 3 or > 3

Python server for: https://github.com/simonvanbennekom/adaguc-webmapjs-sld

## Clone adaguc-webmapjs-sld-server

git clone https://github.com/simonvanbennekom/adaguc-webmapjs-sld-server.git


## Create Python env and installing Librarys

Run the following commands:

1. cd adaguc-webmapjs-sld-server
2. bash bashCreateEnv.sh
3. source env/bin/activate
4. pip install Flask
5. pip install flask-cors
6. pip install configparser
7. pip install sys
8. pip install os
9. pip install glob
10. pip install lxml


To close the env run the following command:

1. deactivate

## Run Server.py

From your project root;

1. source env/bin/activate
2. bash bashRunFlask.sh

Default debugging is off, edit the bashRunFlask.sh file to enable debugging
