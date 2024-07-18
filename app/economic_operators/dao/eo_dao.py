import mysql.connector
import json
from app.config import Config

def get_db_connection():
    return mysql.connector.connect(
        host=Config.MYSQL_HOST,
        user=Config.MYSQL_USER,
        password=Config.MYSQL_PASSWORD,
        database=Config.MYSQL_DB
    )

def execute_procedure(procedure_name, params):
    db = get_db_connection()
    cursor = db.cursor()
    try:
        cursor.callproc(procedure_name, params)
        results = []
        for result in cursor.stored_results():
            fetched_result = result.fetchall()
            if fetched_result:
                json_response_str = fetched_result[0][0]
                results.append(json.loads(json_response_str))
        cursor.close()
        db.close()
        return results[0] if results else {}
    except Exception as e:
        cursor.close()
        db.close()
        raise e

def get_api_secret(api_key):
    result = execute_procedure('user_get_secret', (api_key,))
    return result.get('response').get('api_secret')

def user_authenticate(users_id):
    execute_procedure('user_authenticate', (users_id,))
    
def get_user_id_from_api_key(api_key):
    result = execute_procedure('get_user_id_from_api_key', (api_key,))
    return result.get('usersId')

def execute_login_procedure(data):
    return execute_procedure('login', (data['username'], data['password'], data['lang'],))

def execute_eo_register_procedure(data):
    return execute_procedure('EO_register', (data['param1'], data['param2'], ...))

def execute_eo_update_procedure(eo_id, data):
    return execute_procedure('EO_update', (eo_id, data['param1'], data['param2'], ...))

def execute_eo_delete_procedure(eo_id):
    return execute_procedure('EO_delete', (eo_id,))

def execute_eo_query_list_procedure():
    return execute_procedure('EO_query_list', ('923c8218-4426-11ef-b243-0242ac110002', 'tt'))

def execute_eo_query_details_procedure(eo_id):
    return execute_procedure('EO_query', (eo_id,))