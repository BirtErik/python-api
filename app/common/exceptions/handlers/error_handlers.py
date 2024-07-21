from flask import jsonify
from app.common.exceptions.exceptions import (
    InvalidAuthorizationHeader, 
    Unauthorized, 
    BaseError, 
    DatabaseError
)

def handle_base_error(e):
    response = e.to_dict()
    return jsonify(response), 500

def handle_invalid_authorization_header(e):
    response = e.to_dict()
    return jsonify(response), 400

def handle_unauthorized(e):
    response = e.to_dict()
    return jsonify(response), 401

def handle_database_error(e):
    response = e.to_dict()
    return jsonify(response), 500

def register_error_handlers(app):
    app.register_error_handler(BaseError, handle_base_error)
    app.register_error_handler(InvalidAuthorizationHeader, handle_invalid_authorization_header)
    app.register_error_handler(Unauthorized, handle_unauthorized)
    app.register_error_handler(DatabaseError, handle_database_error)