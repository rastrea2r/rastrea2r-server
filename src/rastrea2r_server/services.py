import logging
import subprocess
from flask import jsonify, request
from rastrea2r_server import app, auth, config, errors
from time import gmtime, strftime
import json
import traceback

# Setup
logger = logging.getLogger(__name__)
app_name = config["rastrea2r"]["app_name"]
rules_location = config["rastrea2r"]["rules_location"]
results_location = config["rastrea2r"]["results_location"]

# http://localhost:5000/test unauthenticated response of "Hello World"
@app.route("/test", methods=["GET"])
def app_test():
    """ Test Method, no authentication required """
    logger.info("Hello World Requested")
    response = {"message": "Hello World!", "status": "200"}
    return jsonify(response)


# Call echo shell cmd on message via /musc/api/v1.0/echo?message=testing
@app.route("/" + app_name + "/api/v1.0/echo", methods=["GET"])
@auth.login_required
def app_echo():
    """ Runs the echo command with input 'message'
        Note: Input is validated and escaped properly
    """
    message = request.args.get("message", "")
    if message:
        p = subprocess.Popen(
            ["echo", message], stdout=subprocess.PIPE, universal_newlines=True
        )
        uptime = p.stdout.readlines()[0].strip()
        response = {"message": uptime, "status": "200"}
        return jsonify(response)
    else:
        return jsonify({"error": "Must provide message attribute via GET"})


# Info method, Return Request Data back to client as JSON
@app.route("/" + app_name + "/api/v1.0/info", methods=["GET"])
@auth.login_required
def app_getinfo():
    """ Returns Flask API Info """
    response = dict()
    response["message"] = "Flask API Data"
    response["status"] = "200"
    response["method"] = request.method
    response["path"] = request.path
    response["remote_addr"] = request.remote_addr
    response["user_agent"] = request.headers.get("User-Agent")

    # GET attributes
    for key in request.args:
        response["GET " + key] = request.args.get(key, "")

    return jsonify(response)


@app.route("/")
def app_index():
    """Index identifying the server"""
    response = {
        "message": app_name + " api server: Authentication required for use",
        "status": "200",
    }
    return jsonify(response)


# Method to serve a yara rule to the REST client. Rulename (filename) must exist on the same directory
@app.route("/" + app_name + "/api/v1.0/rule", methods=["GET"])
@auth.login_required
def get_rule():
    """Fetches the Yara rule requested from Rules directory """
    rulename = request.args.get("rulename", "")
    logger.debug("Pulling " + rulename)
    try:
        rule_file = rules_location + "/" + rulename
        logger.debug("Rule file:" + rule_file)
        f = open(rule_file, "rb")
        rule = f.read()
        f.close()
        return rule
    except:
        return errors.not_found("description : Invalid Rule Requested")


""" Method to post client data from file/dir scan to the REST server. Timestamps written in GMT """


@app.route("/" + app_name + "/api/v1.0/results", methods=["POST"])
@auth.login_required
def post_results():
    """ Gets Results from client and stores them in JSON files """
    module_name = request.headers['module']
    if module_name is None:
        module_name = 'results'

    ip_addr = request.remote_addr
    if ip_addr is None:
        ip_addr = 'NoIp'
    else:
        ip_addr = ip_addr.replace('.','_')

    output_filename = (
        results_location
        + "/"
        + ip_addr +"-"
        + module_name +"-"
        + strftime("%Y-%m-%d-%H%M%S", gmtime())
        + ".json"
    )
    try:
        with open(output_filename, "w") as outfile:
            outfile.write(request.get_json(force=True))
            #json.dump(request.get_json(force=True), outfile)
            response = {"message": "Results Saved Successfully", "status": "200"}
            return jsonify(response)
    except IOError:
        logger.error("\nError: The output file requested doesn't exist\n")
        return errors.internal_error(
            "Error while creating result json file in the server"
        )
