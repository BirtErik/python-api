import hashlib
import hmac
import datetime
from app.economic_operators.dao.eo_dao import (
    get_api_secret, 
    get_user_id_from_api_key, 
    user_authenticate, 
    execute_login_procedure as login_user
)#TODO: Add this to a service, don't call dao directly

from app.utils.aws4_signature import (
    create_canonical_request,
    create_string_to_sign,
    calculate_signature,
    hash_payload
)

def authenticate_request(headers, method, uri, payload):
    authorization_header = headers.get('Authorization')
    
    print(authorization_header)
    
    if not authorization_header:
        return False
    
    auth_parts = authorization_header.split(',')
    if len(auth_parts) != 3:
        raise Exception("Invalid Authorization header format")

    auth_dict = {}
    for part in auth_parts:
        key, value = part.split('=')
        auth_dict[key.strip()] = value.strip()
    
    
    api_key = auth_dict.get('AWS4-HMAC-SHA256 Credential').split('/')[0]
    sent_signature = auth_dict.get('Signature')
    
    api_secret = get_api_secret(api_key)
    if not api_secret:
        return False
    
    request_date = headers.get('X-Amz-Date')
    if not request_date:
        return False
    
    #TODO: CHECK THIS, This is an "example credential scope"
    date_stamp = request_date[:8]
    credentials_scope = f"{date_stamp}/us-east-1/execute-api/aws4_request"
    
    #Creating canonical request
    query_string = ''
    payload_hash = hash_payload(payload)
    canonical_request = create_canonical_request(method, uri, query_string, headers, payload_hash)
    
    sts = create_string_to_sign(canonical_request, request_date, credentials_scope)
    
    print("STS", sts)
    
    calculated_signature = calculate_signature(api_secret, date_stamp, 'us-east-1', 'execute-api', sts)
    #print(sent_signature)
    #print(calculated_signature)
    if hmac.compare_digest(calculated_signature, sent_signature):
        users_id = get_user_id_from_api_key(api_key)
        user_authenticate(users_id)
        return True
    
    return False

def process_login(data):
    login_result = login_user(data)
    api_key = login_result.get('response').get('api_key')

    api_secret = get_api_secret(api_key)
    if not api_secret:
        raise Exception('Api_secret not found')

    users_id = get_user_id_from_api_key(api_key)
    #user_authenticate(users_id)

    response = {
        "response": {
            "status": login_result.get("status"),
            "errorCode": login_result.get("errorCode"),
            "errorMessage": login_result.get("errorMessage"),
            "api_key": api_key,
            "api_secret": api_secret,
            "timestamp": login_result.get("timestamp")
        }
    }

    return response

'''
def process_login(data, headers):
    login_resault = login_user(data)
    api_key = login_resault.get('response').get('api_key')
    
    api_secret = get_api_secret(api_key)
    if not api_secret:
        #TODO: Check errors 
        raise Exception('Api_secret not found')
    
    authorization_header = headers.get('Authorization')
    if not authorization_header:
        raise Exception("Authorization header not found")
    
    auth_parts = authorization_header.split(',')
    if len(auth_parts) != 3:
        raise Exception("Invalid Authorization header format")

    auth_dict = {}
    for part in auth_parts:
        key, value = part.split('=')
        auth_dict[key.strip()] = value.strip()
    
    sent_signature = auth_dict.get('Signature')
    
    request_date = headers.get('X-Amz-Date')
    if not request_date:
        raise Exception("x-amz-date header not found")
    
    date_stamp = request_date[:8]
    credential_scope = f"{date_stamp}/us-east-1/execute-api/aws4_request"
    
    query_string = ''
    payload_hash = hash_payload("")
    canonical_request = create_canonical_request("POST", "/tpd/v1/login", query_string, headers, payload_hash)
    
    sts = create_string_to_sign(canonical_request, request_date, credential_scope)
    
    calculated_signature = calculate_signature(api_secret, date_stamp, 'us-east-1', 'execute-api', sts)
    
    if hmac.compare_digest(calculated_signature, sent_signature):
        users_id = get_user_id_from_api_key(api_key)
        user_authenticate(users_id)
        print("TU SAM")
        #TODO: Add this to a function
        response = {
            "response": {
                "status": login_resault.get("status"),
                "errorCode": login_resault.get("errorCode"),
                "errorMessage": login_resault.get("errorMessage"),
                "api_key": api_key,
                "api_secret": api_secret,
                "timestamp": login_resault.get("timestamp")
            }
        }
        
        return response

    raise Exception("Invalid signature")
    '''