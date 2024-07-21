from flask import Flask, jsonify
from .config import Config
from .economic_operators.controllers import eo_controller
from app.common.exceptions.handlers.error_handlers import register_error_handlers
from .common.auth.controllers import auth_controller

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.register_blueprint(eo_controller.api_blueprint, url_prefix='/tpd/v1')
    app.register_blueprint(auth_controller.api_auth, url_prefix='/tpd/v1')
    
    register_error_handlers(app)
 
    return app