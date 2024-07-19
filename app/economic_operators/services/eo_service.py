from app.economic_operators.dao.eo_dao import (
    execute_login_procedure,
    execute_eo_update_procedure,
    execute_eo_delete_procedure,
    execute_eo_query_details_procedure,
    execute_eo_query_list_procedure,
    execute_eo_register_procedure,
)
from app.common.auth.services.auth_service import process_login

def user_login(headers, method, uri, payload):
    return process_login(headers, method, uri, payload);


def queryEoList():
    return execute_eo_query_list_procedure()