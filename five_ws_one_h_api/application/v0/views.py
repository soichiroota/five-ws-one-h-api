from flask import Blueprint, jsonify, request
from five_ws_one_h_api.five_ws_one_h import main

v0_blueprint = Blueprint("v0", __name__)


@v0_blueprint.route("/v0", methods=["post"])
def post():
    json_data = request.get_json()

    data = main(json_data["text"])

    response = dict(data=data)
    return jsonify(response)
