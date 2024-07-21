from app.common.utils.db_utils import execute_procedure

def execute_user_get_secret(api_key):
    return execute_procedure('user_get_secret', (api_key,))

def execute_user_authenticate(users_id):
    execute_procedure('user_authenticate', (users_id,))
    
def execute_get_user_id_from_api_key(api_key):
    result = execute_procedure('get_user_id_from_api_key', (api_key,))
    return result['response']['usersId']

def execute_check_user_authentication(users_id):
    return execute_procedure('check_user_authentication', (users_id,))

def execute_login_procedure(data, api_log_path):
    return execute_procedure('user_login', (data['username'], data['password'], data['lang'], api_log_path, ))