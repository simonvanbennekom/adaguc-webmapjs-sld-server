# adaguc-webmapjs-sld-server
Python server for: https://github.com/simonvanbennekom/adaguc-webmapjs-sld

## Clone adaguc-webmapjs-sld-server


git clone https://github.com/simonvanbennekom/adaguc-webmapjs-sld-server.git


## Create Python env


Run the following commands:

1. cd adaguc-webmapjs-sld-server/bashScripts
2. bash env.sh
3. cd ../
4. source env/bin/activate
5. pip install Flask

To close the env run the following command:

1. deactivate

## Run Server.py

1. export FLASK_APP=Server.py

* **Run with debug** 
    * export FLASK_ENV=development

2. flask run
