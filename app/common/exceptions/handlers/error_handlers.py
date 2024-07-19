from flask import jsonify
from app.common.exceptions.exceptions import InvalidAuthorizationHeader, Unauthorized
from app.common.exceptions.db_exceptions import DatabaseError

def handle_exception(e):
    response = {
        "error": str(e)
    }
    return jsonify(response), 500

def handle_invalid_authorization_header(e):
    response = {
        "error": e.message
    }
    return jsonify(response), 400

def handle_401_error(e):
    response = {"error": ""}
    
    if e:
        response['error'] = e.message
    else:
        response['error'] = "Unauthorized access"
    
    return jsonify(response), 401

def handle_database_error(e):
    response = {
        "status": e.status,
        "errorCode": e.error_code,
        "errorMessage": e.error_message,
        "timestamp": e.timestamp
    }
    return jsonify(response), 500

def register_error_handlers(app):
    app.register_error_handler(Exception, handle_exception)
    app.register_error_handler(InvalidAuthorizationHeader, handle_invalid_authorization_header)
    app.register_error_handler(401, handle_401_error)
    app.register_error_handler(Unauthorized, handle_401_error)
    app.register_error_handler(DatabaseError, handle_database_error)