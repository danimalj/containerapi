# Project Title

This project sets up a fastapi apis and a postgres database.  Using docker-compose, it will create two api servers, an nginx load balancer, and a database server. It is intended to show how to create a simple load balanced api across containers that can be extended and deployed.

## Installation

It is assumed that python and some form of container tool like docker desktop or rancher is installed locally.

# Clone the repository
git clone https://github.com/danimalj/containerapi.git

# Navigate to the project directory

cd containerapi

# Set up a python virtual environment for testing

create a python virtual environment

python -m venv .venv
.venv/scripts/activate
pip install -r requirements.txt

# Deploy the containers

Ensure your container management tool is running on the machine.

docker-compose up --build -d

# Run a test load

This test will call multiple tests through the api including:

* Load 100 records
* Retrieve a single record
* Retrieve 100 records in bulk
* Update 10 records
* Get a summary of data from the table
* Delete the test records

pytest test_api.py -v

# Run a bulk load of data

A bulk load utility has been built to load data into the database. If no parameter is provided it will automatically load 100 records. Otherwise a specific number of records can be loaded.

usage: load_data.py [-h] [--records RECORDS]

Load data into the database.

options:
  -h, --help         show this help message and exit
  --records RECORDS  Number of records to insert

# Calling the API through a browser.

## GET

curl http://localhost:8080/records
curl http://localhost:8080/records?records=20
curl http://localhost:8080/records?record_id=<record_id>

## POST

curl -X POST http://localhost:8080/records \
-H "Content-Type: application/json" \
-d '{"text": "Your record text here"}'

## PUT

curl -X PUT http://localhost:8080/records/<record_id> \
-H "Content-Type: application/json" \
-d '{"updated_text": "New text content here"}'

## DELETE

curl -X DELETE http://localhost:8080/records/delete/<record_id> \
-H "Content-Type: application/json"

# Credentials

While default usernames and passwords have been provided in the configuration, please change them if you plan to use this.  Look in the docker-compose file for details.