from flask import Blueprint, request, jsonify, abort
from app.economic_operators.services.eo_service import (
    user_login,
    queryEoList
)
from app.common.auth.services.auth_service import (
    authenticate_request,
)

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('login', methods=['POST'])
def login():
    try:
        result = user_login(request.headers, request.method, request.path, request);
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)})
  
@api_blueprint.route('/eolist', methods=['GET'])
def query_economic_operator_list():
    if not authenticate_request(request.headers, request.method, request.path, request):
        abort(401)

    result = queryEoList()
    return jsonify(result), 200
 
    
@api_blueprint.errorhandler(401)
def unauthorized(e):
    return jsonify(message="Unauthorized"), 401
