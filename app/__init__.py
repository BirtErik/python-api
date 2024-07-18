from flask import Flask
from .config import Config
from .economic_operators.controllers import eo_controller

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(eo_controller.api_blueprint, url_prefix='/tpd/v1')
    
    return app