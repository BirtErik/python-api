from flask import jsonify
from app.common.exceptions.exceptions import (
    InvalidAuthorizationHeader, 
    Unauthorized, 
    BaseError, 
    NotFound,
    DatabaseError
)
import logging

def log_exception(e):
    logger = logging.getLogger()
    logger.error(f"Exception: {str(e)}")

def handle_base_error(e):
    log_exception(e)
    response = e.to_dict()
    return jsonify(response), 500

def handle_invalid_authorization_header(e):
    log_exception(e)
    response = e.to_dict()
    return jsonify(response), 400

def handle_unauthorized(e):
    log_exception(e)
    response = e.to_dict()
    return jsonify(response), 401

def handle_not_found(e):
    log_exception(e)
    response = e.to_dic()
    return jsonify(response), 404

def handle_database_error(e):
    log_exception(e)
    response = e.to_dict()
    return jsonify(response), 500

def register_error_handlers(app):
    app.register_error_handler(BaseError, handle_base_error)
    app.register_error_handler(InvalidAuthorizationHeader, handle_invalid_authorization_header)
    app.register_error_handler(Unauthorized, handle_unauthorized)
    app.register_error_handler(NotFound, handle_not_found)
    app.register_error_handler(DatabaseError, handle_database_error)