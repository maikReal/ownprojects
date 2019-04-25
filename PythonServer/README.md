# About Python Server
The realisation of such server is very easy. I took `Flask` library for `Python3`, write basic logic for two GET requests:<br>
1. GET /api/v1/get_rabbit -> installing `Standalone RabbitMQ`
2. GET /api/v1/get_mongo -> installing `MongoDB` <br>
Every template shows the work shell script for installing of the different apps (`MongoDB` or `Standalone RabbitMQ`). The main logic located in `server.py` file and templates with shell scripts are located in folder `templates`

# Dockerfile
Defining of Dockerfile is happening in `Dockerfile`. Here is written the installing of dependences, changing of workspace and starting the `PythonServer`. All dependences are situated in `requirments.txt` file.

# Using
Requirments: <br>
1. `docker client`
2. `docker-compose` <br>
For using `PythonServer` clone this repo, got ot this folder and use next command:
`docker-compose up` <br>
After this Dockerfile will build and start
