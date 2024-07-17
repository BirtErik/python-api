from flask import Flask, jsonify
import mysql.connector
import json

app = Flask(__name__)

db = mysql.connector.connect(
    host="localhost",
    user="erik",
    password="admin",
    database="test"
)
cursor = db.cursor()

@app.route('/test')
def test():
    cursor.callproc('EO_register', ('test', 'test', 'test', 'test', 'test', 'test', 'test', 'HR', 
	'test', 'test', 'test', 1, 'Test', None, 1, 'test', 1, 'test', 
	1, 'test', None, None, 1, '4cd10f06-4381-11ef-beb6-0242ac110002', 'I_API_LOG_PATH_TEST'))
    
    res = {};
    
    for result in cursor.stored_results():
        fetched_result = result.fetchall()
        if fetched_result:
            # Fetch the first row (there should only be one row)
            json_response_str = fetched_result[0][0]
            # Parse the JSON string
            res = json.loads(json_response_str)
    
    cursor.close()
    
    return jsonify(res)

@app.route('/list')
def query_list():
    cursor.callproc('query_eolist', ('4cd10f06-4381-11ef-beb6-0242ac110002', 'api_log'))
    res = {};
    
    for result in cursor.stored_results():
        fetched_result = result.fetchall()
        if fetched_result:
            # Fetch the first row (there should only be one row)
            json_response_str = fetched_result[0][0]
            # Parse the JSON string
            res = json.loads(json_response_str)
    
    cursor.close()
    
    return jsonify(res)
    

if __name__ == "__main__":
    app.run(port=5001, debug=True)