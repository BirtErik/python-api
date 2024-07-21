from flask import Blueprint, request, jsonify
from app.economic_operators.services.eo_service import (
    eo_register,
    eo_update,
    query_eo_list,
    query_eo_list_details,
)

api_blueprint = Blueprint('api', __name__)

@api_blueprint.route('eo', methods=['POST'])
def create():
    result = eo_register(request)
    return jsonify(result), 200

@api_blueprint.route('/eo/<string:eo_id>', methods=['PUT'])
def update(eo_id):
    result = eo_update(request, eo_id)
    return jsonify(result), 200

@api_blueprint.route('/eolist', methods=['GET'])
def query_economic_operator_list():
    result = query_eo_list(request)
    return jsonify(result), 200

@api_blueprint.route('/eolist/<string:eo_id>', methods=['GET'])
def query_economic_operator_details(eo_id):
    result = query_eo_list_details(request, eo_id)
    return jsonify(result), 200
