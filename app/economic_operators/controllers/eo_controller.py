from flask import Blueprint, request, jsonify
from app.economic_operators.services.eo_service import (
    eo_register,
    eo_update,
    eo_delete,
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

@api_blueprint.route('/eo/<string:eo_id>', methods=['DELETE'])
def delete(eo_id):
    result = eo_delete(request, eo_id)
    return jsonify(result), 200

@api_blueprint.route('/eolist', methods=['GET'])
def query_list():
    result = query_eo_list(request)
    return jsonify(result), 200

@api_blueprint.route('/eolist/<string:eo_id>', methods=['GET'])
def query_details(eo_id):
    result = query_eo_list_details(request, eo_id)
    return jsonify(result), 200
