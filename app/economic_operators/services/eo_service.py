from flask import abort

from app.economic_operators.dao.eo_dao import (
    execute_get_user_id_from_api_key,
    execute_eo_update_procedure,
    execute_eo_delete_procedure,
    execute_eo_query_details_procedure,
    execute_eo_query_list_procedure,
    execute_eo_register_procedure,
)
from app.common.auth.services.auth_service import process_login, authenticate_request as auth_request
from app.common.exceptions.exceptions import Unauthorized, BaseError
from app.common.utils.utils import extract_api_key, extract_auth_header

def get_user_id(headers):
    api_key = extract_api_key(headers)
    return execute_get_user_id_from_api_key(api_key)

def authenticate_request(request):
    if not auth_request(request.headers, request.method, request.path, request):
        raise(Unauthorized)

def get_authenticated_user_id(request):
    authenticate_request(request)
    user_id = get_user_id(request.headers)
    return user_id

def user_login(request):
    return process_login(request.headers, request.method, request.path, request);

def eo_register(request):
    user_id = get_authenticated_user_id(request)
    data = request.get_json()
    return execute_eo_register_procedure(data['request'], user_id, 'api_log')

def eo_update(request, eo_id):
    user_id = get_authenticated_user_id(request)
    data = request.get_json()
    return execute_eo_update_procedure(eo_id, data['request'], user_id,'api_log')

def query_eo_list(request):
    user_id = get_authenticated_user_id(request)
    return execute_eo_query_list_procedure(user_id, 'log_path')

def query_eo_list_details(request, eo_id):
    user_id = get_authenticated_user_id(request)
    return execute_eo_query_details_procedure(eo_id, user_id, 'log_path')