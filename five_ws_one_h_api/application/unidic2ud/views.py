from flask import Blueprint, jsonify, request
from five_ws_one_h_api.five_ws_one_h.unidic2ud import main

unidic2ud_blueprint = Blueprint("unidic2ud", __name__)


@unidic2ud_blueprint.route("/unidic2ud", methods=["post"])
def post():
    json_data = request.get_json()

    data = main(json_data["text"])

    response = dict(data=data)
    return jsonify(response)
