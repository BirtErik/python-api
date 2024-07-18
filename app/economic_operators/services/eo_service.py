from app.economic_operators.dao.eo_dao import (
    execute_login_procedure,
    execute_eo_update_procedure,
    execute_eo_delete_procedure,
    execute_eo_query_details_procedure,
    execute_eo_query_list_procedure,
    execute_eo_register_procedure,
)

def login(data):
    return execute_login_procedure(data)

def queryEoList():
    return execute_eo_query_list_procedure()