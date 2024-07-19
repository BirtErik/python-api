import hashlib
import hmac
import datetime
from app.economic_operators.dao.eo_dao import (
    get_api_secret, 
    get_user_id_from_api_key, 
    user_authenticate, 
    execute_login_procedure as login_user
)#TODO: Add this to a service, don't call dao directly

from app.common.utils.aws4_signature import (
    create_canonical_request,
    create_string_to_sign,
    calculate_signature,
    hash_payload
)

from app.common.exceptions.exceptions import InvalidAuthorizationHeader, Unauthorized

def authenticate_request(headers, method, uri, payload):
    authorization_header = headers.get('Authorization')
    
    if not authorization_header:
        raise InvalidAuthorizationHeader()
    
    auth_parts = authorization_header.split(',')
    if len(auth_parts) != 3:
        raise InvalidAuthorizationHeader()

    auth_dict = {}
    for part in auth_parts:
        key, value = part.split('=')
        auth_dict[key.strip()] = value.strip()
    
    credential_part = auth_dict.get('AWS4-HMAC-SHA256 Credential')
    if not credential_part:
        raise InvalidAuthorizationHeader()
    
    api_key = credential_part.split('/')[0]
    sent_signature = auth_dict.get('Signature')
    
    api_secret_result = get_api_secret(api_key)
    api_secret = api_secret_result['response']['api_secret']
    
    if not api_secret:
        return False
    
    request_date = headers.get('X-Amz-Date')
    if not request_date:
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
    
    if hmac.compare_digest(calculated_signature, sent_signature):
        return True
    
    return False

def process_login(headers, method, uri, payload):
    if not authenticate_request(headers, method, uri, payload):
        raise Unauthorized()
    
    data = payload.get_json();
    
    login_result = login_user(data)
    api_key = login_result['response']['api_key']
    
    api_secret_result = get_api_secret(api_key)
    api_secret = api_secret_result['response']['api_secret']
        
    if not api_secret:
        raise Exception('Api_secret not found')

    users_id = get_user_id_from_api_key(api_key)
    #TODO: ADD USER_AUTHENTICATE LOGIC
    #user_authenticate(users_id)

    response = {
        "response": {
            "status": api_secret_result['response']['status'],
            "errorCode": api_secret_result['response']['errorCode'],
            "errorMessage": api_secret_result['response']['errorMessage'],
            "api_key": api_key,
            "api_secret": api_secret,
            "timestamp": api_secret_result['response']['timestamp']
        }
    }

    return response
