rastrea2r-server
###############

Flask based Restful Server to handle requests from rastrea2r


Quickstart
==========

## Requirements
* Python 3.4+
* VirtualEnv

## Features
* Sample Rest Client
* Strong Password Hashing (stored in sqlite DB)
* Rate limiting for safety
* JSONified error handling
* Extensive logging to both stdout and log files

## Installing
* Make sure you have virtualenv and Python3 installed on your system (pip3 install virtualenv)
* Clone the repo: ```https://github.com/rastrea2r/rastrea2r-server.git```
* Install the virtualenv: ```cd rastrea2r; python3 -m virtualenv venv```
* Activate the virtual environment: ```source venv/bin/activate```
* Install Python Requirements: ```pip3 install -r requirements.txt```

## Testing
* You must activate the virtualenv before starting the server
* Initialize DB and Add a user: 
.. code-block:: console
    ./manage_server.py --init
	./manage_server.py --add testuser 


* Start the server: 
.. code-block:: console
    ./start_server.py

* Test the info request with a browser:
.. code-block:: console
    http://localhost:5000/
    http://localhost:5000/rastrea2r/api/v1.0/info
    http://localhost:5000/rastrea2r/api/v1.0/echo?message=test
    http://localhost:5000/rastrea2r/api/v1.0/uptime
    http://localhost:5000/test
    
* Or you could use curl
.. code-block:: console
    curl -d '{"key1":"value1", "key2":"value2"}' -H "Content-Type: application/json" -H "Authorization: Basic dGVzdHVzZXI6dGVzdHBhc3N3ZA==" -X POST http://localhost:5000/rastrea2r/api/v1.0/results

    curl -H "Authorization: Basic dGVzdHVzZXI6dGVzdHBhc3N3ZA=="  http://localhost:5000/rastrea2r/api/v1.0/rule?rulename=example.yara

    Note: Basic auth uses the base64 encoded string corresponding to username:password (in this case the username:password combo used was testuser:testpasswd)

The `API Reference <http://rastrea2r_server.readthedocs.io>`_ provides API-level documentation.
