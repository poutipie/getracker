from getracker import app, db
from .commons import Commons

import requests
from flask import jsonify, request

@app.route("/api/<path:any_match>")
def api(any_match):

    api_path = request.full_path[5:]
    api_url= "{}/{}".format(Commons._OSRS_API, api_path)

    response = requests.get(api_url)
    
    if response.status_code ==requests.codes.ok:
        return jsonify(response.json())
    return "invalid API path"
    