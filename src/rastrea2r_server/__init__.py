#!/usr/bin/env python
"""
Flask API Server
"""
import sys
import os
import re
import logging
from logging.handlers import RotatingFileHandler
import configparser
from flask import Flask, jsonify, request, g, make_response
from flask_httpauth import HTTPBasicAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy

__version__ = "0.0.1"

logger = logging.getLogger(__name__)

# Populated from config file
debug = 0

# Flask Limits for Safety
flask_limits = ["1000 per day", "100 per hour", "5 per minute"]


def override_config(cfg):
    """ Override/Add config file variables from environment
        Note: Only adds variables if [section] exists
    """

    for en in os.environ:
        oride = re.search(r"^RASTREA2R_([a-zA-Z]+)_(\w+)", en)
        if oride:
            if oride.group(1) in cfg:
                # print('RASTREA2R Override', oride.group(1), oride.group(2), os.environ[en])
                cfg[oride.group(1)][oride.group(2)] = os.environ[en]

    return cfg


# Initialize Configuration
config_file = "rastrea2r.ini"

# Environment Override
if "RASTREA2R_config_file" in os.environ:
    config_file = os.environ["RASTREA2R_config_file"]

config = configparser.ConfigParser()
config.read(config_file)

# Override config file from environment variables
config = override_config(config)


# Check for sane config file
if "rastrea2r" not in config:
    print("Could not parse config file: " + config_file)
    sys.exit(1)

# Logging Configuration, default level INFO
logger = logging.getLogger("")
logger.setLevel(logging.INFO)
lformat = logging.Formatter("%(asctime)s %(name)s:%(levelname)s: %(message)s")

# Debug mode Enabled
if "debug" in config["rastrea2r"] and int(config["rastrea2r"]["debug"]) != 0:
    debug = int(config["rastrea2r"]["debug"])
    logger.setLevel(logging.DEBUG)
    logging.debug("Enabled Debug mode")

# Enable logging to file if configured
if "logfile" in config["rastrea2r"]:
    lfh = RotatingFileHandler(
        config["rastrea2r"]["logfile"], maxBytes=(1048576 * 5), backupCount=3
    )
    lfh.setFormatter(lformat)
    logger.addHandler(lfh)

# STDOUT Logging defaults to Warning
if not debug:
    lsh = logging.StreamHandler(sys.stdout)
    lsh.setFormatter(lformat)
    lsh.setLevel(logging.WARNING)
    logger.addHandler(lsh)

# Create Flask APP
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(
    dict(
        DATABASE=os.path.join(app.root_path, config["rastrea2r"]["database"]),
        SQLALCHEMY_DATABASE_URI="sqlite:///"
        + os.path.join(app.root_path, config["rastrea2r"]["database"]),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
)

# Auth module
auth = HTTPBasicAuth()

# Database module
db = SQLAlchemy(app)

# Apply Rate limiting
limiter = Limiter(app, key_func=get_remote_address, global_limits=flask_limits)

# Not Required with SQLAlchemy
# @app.teardown_appcontext
# def close_db(error):
#     """Closes the database again at the end of the request."""
#     db.remove()


# Safe circular imports per Flask guide
import rastrea2r_server.errors
import rastrea2r_server.services
import rastrea2r_server.user
