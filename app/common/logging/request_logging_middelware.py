from flask import request
import logging

def log_request():
    logger = logging.getLogger()
    logger.info(f"Request: {request.method} {request.url} - {request.remote_addr}")
    
def log_user_login(user_id):
    logger = logging.getLogger()
    logger.info(f"User Login: {user_id} - {request.remote_addr}")
    
def log_user_authentication(user_id, message):
    logger = logging.getLogger()
    logger.info(f"{message}: {user_id} - {request.method} {request.url}")