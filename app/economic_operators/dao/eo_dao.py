from app.common.utils.db_utils import execute_procedure

def build_eo_params(data, users_id, api_log_path, eo_id=None):
    
    params = [
        data['EO_Name1'],
        data['EO_Name2'],
        data['EO_Address_Name'],
        data['EO_Address_StreetOne'],
        data['EO_Address_StreetTwo'],
        data['EO_Address_City'],
        data['EO_Address_PostCode'],
        data['EO_CountryReg'],
        data['EO_Email'],
        data['EO_Phone'],
        data['EO_A_Info'],
        data['VAT_R'],
        data['VAT_N'],
        data['TAX_N'],
        data['EO_ExciseNumber1'],
        data['EO_ExciseNumber2'],
        data['OtherEOID_R'],
        data['OtherEOID_N_list'],
        data['Reg_3RD'],
        data['Reg_EOID'],
        data['EO_OtherID'],
        data['Extensibility'],
        data['EO_Type'],
    ]
    
    if 'EO_CODE' in data:
        params.append(data['EO_CODE'])

    params.append(users_id)
    params.append(api_log_path)

    if eo_id is not None:
        params.insert(0, eo_id)

    return tuple(params)

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

def execute_eo_register_procedure(data, users_id, api_log_path):
    params = build_eo_params(data, users_id, api_log_path)
    return execute_procedure('EO_register', params)

def execute_eo_update_procedure(eo_id, data, users_id, api_log_path):
    params = build_eo_params(data, users_id, api_log_path, eo_id)
    return execute_procedure('EO_update', params)

def execute_eo_delete_procedure(eo_id):
    return execute_procedure('EO_delete', (eo_id,))

def execute_eo_query_list_procedure(user_id, api_log_path):
    return execute_procedure('EO_query_list', (user_id, api_log_path))

def execute_eo_query_details_procedure(eo_id, user_id, api_log_path):
    return execute_procedure('EO_query', (eo_id, user_id, api_log_path, ))