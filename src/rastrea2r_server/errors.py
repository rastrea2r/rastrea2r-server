import logging
from flask import Flask, jsonify, request, g, make_response
from rastrea2r_server import app, auth

logger = logging.getLogger(__name__)


@app.errorhandler(404)
def not_found(error=None):
    message = {"status": 404, "message": "Not Found: " + str(error)}
    resp = jsonify(message)
    resp.status_code = 404
    return resp


@app.errorhandler(429)
def ratelimit_handler(e):
    return make_response(jsonify(error="ratelimit exceeded %s" % e.description), 429)


@auth.error_handler
def auth_failed(error=None):
    message = {"status": 401, "message": "Authentication Failed: " + request.url}
    resp = jsonify(message)
    resp.status_code = 401
    return resp


@app.errorhandler(400)
def bad_request(error):
    print("Bad Request")
    message = {"status": 400, "message": "Bad Request: " + request.url}
    resp = jsonify(message)
    resp.status_code = 400
    return resp

@app.errorhandler(405)
def method_not_allowed(error):
    print("Method Not Allowed")
    message = {"status": 405, "message": "Method Not Allowed: " + request.url}
    resp = jsonify(message)
    resp.status_code = 405
    return resp

@app.errorhandler(500)
def internal_error(error):
    print("Internal Error")
    message = {"status": 500, "message": "Internal Error: " + str(error)}
    resp = jsonify(message)
    resp.status_code = 500
    return resp