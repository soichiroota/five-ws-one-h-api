import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_debugtoolbar import DebugToolbarExtension

# instantiate the extensions
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()


def create_app(script_info=None):

    # instantiate the app
    app = Flask(__name__)

    # set config
    app_settings = os.getenv("APP_SETTINGS", "five_ws_one_h_api.config.ProductionConfig")
    app.config.from_object(app_settings)

    # set up extensions
    toolbar.init_app(app)
    bootstrap.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # register blueprints
    from five_ws_one_h_api.application.health_checks.views import health_check_blueprint
    from five_ws_one_h_api.application.v0.views import v0_blueprint
    from five_ws_one_h_api.application.unidic2ud.views import unidic2ud_blueprint

    app.register_blueprint(health_check_blueprint)
    app.register_blueprint(v0_blueprint, url_prefix="/api")
    app.register_blueprint(unidic2ud_blueprint, url_prefix="/api")

    return app
