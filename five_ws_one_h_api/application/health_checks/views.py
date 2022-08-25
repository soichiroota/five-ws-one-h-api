from flask import Blueprint, jsonify

health_check_blueprint = Blueprint("health_check", __name__)


@health_check_blueprint.route("/")
def get():
    return jsonify(dict(message="Hello World!"))
