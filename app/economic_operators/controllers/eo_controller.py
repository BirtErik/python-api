from flask import Blueprint, request, jsonify
from app.economic_operators.services.eo_service import (
    login,
    queryEoList
)
from app.economic_operators.services.auth_service import (
    authenticate_request,
    process_login
)

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('login', methods=['POST'])
def login():
    data = request.get_json();
    try:
        result = process_login(data);
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)})
  
@api_blueprint.route('/eolist', methods=['GET'])
def query_economic_operator_list():
    if not authenticate_request(request.headers, request.method, request.path, ''):
        return jsonify({"error": "Unauthorized"}), 401
    try:
        result = queryEoList()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500    