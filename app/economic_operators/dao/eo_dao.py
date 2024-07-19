from app.common.utils.db_utils import execute_procedure

def execute_user_get_secret(api_key):
    return execute_procedure('user_get_secret', (api_key,))

def execute_user_authenticate(users_id):
    execute_procedure('user_authenticate', (users_id,))
    
def execute_get_user_id_from_api_key(api_key):
    result = execute_procedure('get_user_id_from_api_key', (api_key,))
    return result['response']['usersId']

def execute_login_procedure(data):
    return execute_procedure('login', (data['username'], data['password'], data['lang'],))

def execute_eo_register_procedure(data):
    return execute_procedure('EO_register', (data['param1'], data['param2'], ...))

def execute_eo_update_procedure(eo_id, data):
    return execute_procedure('EO_update', (eo_id, data['param1'], data['param2'], ...))

def execute_eo_delete_procedure(eo_id):
    return execute_procedure('EO_delete', (eo_id,))

def execute_eo_query_list_procedure(user_id, api_log_path):
    return execute_procedure('EO_query_list', (user_id, api_log_path))

def execute_eo_query_details_procedure(eo_id, user_id, api_log_path):
    return execute_procedure('EO_query', (eo_id, user_id, api_log_path, ))