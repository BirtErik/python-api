import hmac
from app.auth.dao.auth_dao import (
    execute_user_get_secret, 
    execute_get_user_id_from_api_key, 
    execute_user_authenticate, 
    execute_login_procedure,
    execute_check_user_authentication
)

from app.common.utils.aws4_signature import (
    create_canonical_request,
    create_string_to_sign,
    calculate_signature,
    hash_payload
)

from app.common.exceptions.exceptions import InvalidAuthorizationHeader, Unauthorized
from app.common.utils.utils import extract_api_key, extract_api_secret, extract_auth_header

def check_authentication(api_key):
    users_id = execute_get_user_id_from_api_key(api_key)
    check_auth_response = execute_check_user_authentication(users_id)
    is_authenticated = check_auth_response['response']['isAuthenticated']
    
    return is_authenticated

def create_json_login_response(data, api_key, api_secret):
    response = {
        "response": {
            "status": data['response']['status'],
            "errorCode": data['response']['errorCode'],
            "errorMessage": data['response']['errorMessage'],
            "api_key": api_key,
            "api_secret": api_secret,
            "timestamp": data['response']['timestamp']
        }
    }

    return response

def authenticate_request(headers, method, uri, payload, is_login=False):
    api_key = extract_api_key(headers)
    api_secret = extract_api_secret(api_key)
    
    if not api_secret:
        return False
    
    request_date = headers['X-Amz-Date']
    if not request_date:
        raise InvalidAuthorizationHeader()
    
    content_type = headers['Content-Type']
    if not content_type:
        raise InvalidAuthorizationHeader()
    
    date_stamp = request_date[:8]
    credentials_scope = f"{date_stamp}/us-east-1/execute-api/aws4_request"
    
    
    signed_headers = []
    payload_as_text = payload.get_data(as_text=True)
    if payload_as_text:
        signed_headers.extend(['content-type', 'host', 'x-amz-content-sha256', 'x-amz-date'])
    else:
        signed_headers.extend(['content-type', 'host', 'x-amz-date'])
    
    payload_hash = hash_payload(payload_as_text)
    query_string = '' 
    canonical_request = create_canonical_request(method, uri, query_string, headers, payload_hash, signed_headers)
    
    sts = create_string_to_sign(canonical_request, request_date, credentials_scope)
    
    calculated_signature = calculate_signature(api_secret, date_stamp, 'us-east-1', 'execute-api', sts)
    
    auth_dict = extract_auth_header(headers)
    sent_signature = auth_dict['Signature']
    
    if hmac.compare_digest(calculated_signature, sent_signature):
        if is_login:
            return True
        else:
            return check_authentication(api_key)
    
    return False

def process_login(headers, method, uri, payload):
    if not authenticate_request(headers, method, uri, payload, is_login=True):
        raise Unauthorized()
    
    data = payload.get_json();
    login_result = execute_login_procedure(data['request'], 'api_log_path')
    api_key = login_result['response']['api_key']
    
    api_secret_result = execute_user_get_secret(api_key)
    api_secret = api_secret_result['response']['api_secret']
        
    if not api_secret:
        raise Exception('Api_secret not found')

    users_id = execute_get_user_id_from_api_key(api_key)
    execute_user_authenticate(users_id)

    return create_json_login_response(api_secret_result, api_key, api_secret)

def user_login(request):
    return process_login(request.headers, request.method, request.path, request);