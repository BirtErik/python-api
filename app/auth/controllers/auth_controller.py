from flask import Blueprint, request, jsonify
from app.auth.services.auth_service import user_login

api_auth = Blueprint('api_auth', __name__)

@api_auth.route('login', methods=['POST'])
def login():
    result = user_login(request);
    return jsonify(result), 200
