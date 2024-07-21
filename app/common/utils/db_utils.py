import mysql.connector
import json
from app.config import Config
from app.common.exceptions.exceptions import DatabaseError

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
                json_response = json.loads(json_response_str)
                
                if json_response['response']['errorCode'] != 0:
                    raise DatabaseError(
                        status=json_response['response']['status'],
                        error_code=json_response['response']['errorCode'],
                        error_message=json_response['response']['errorMessage'],
                        timestamp=json_response['response']['timestamp']
                    )
                    
                results.append(json_response)
                
        return results[0] if results else {}
    except DatabaseError as db_err:
        raise db_err
    except mysql.connector.Error as err:
        raise DatabaseError(
            status='Error',
            error_code=err.errno,
            error_message=f'Data error: {str(err.msg)}'
        )
    finally:
        cursor.close()
        db.close()