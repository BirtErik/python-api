from app.common.exceptions.exceptions import InvalidAuthorizationHeader
from app.auth.dao.auth_dao import execute_user_get_secret 

def extract_auth_header(headers):
    authorization_header = headers['Authorization']
    
    if not authorization_header:
        raise InvalidAuthorizationHeader()
    
    auth_parts = authorization_header.split(',')
    if len(auth_parts) != 3:
        raise InvalidAuthorizationHeader()

    auth_dict = {}
    for part in auth_parts:
        key, value = part.split('=')
        auth_dict[key.strip()] = value.strip()
        
    return auth_dict


def extract_api_key(headers):
    auth_dict = extract_auth_header(headers)
    credential_part = auth_dict['AWS4-HMAC-SHA256 Credential']
    if not credential_part:
        raise InvalidAuthorizationHeader()
    
    return credential_part.split('/')[0]

def extract_api_secret(api_key):
    api_secret_result = execute_user_get_secret(api_key)   
    return api_secret_result['response']['api_secret']
    