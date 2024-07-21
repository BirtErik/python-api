import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

def setup_logging(log_dir='logs'):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    current_date = datetime.now().strftime('%d-%m-%Y')
    log_file = os.path.join(log_dir, f'{current_date}.log')
    
    logger = logging.getLogger()
    if not logger.handlers:
        handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=30);
        handler.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        handler.setFormatter(formatter)
        
        logger.setLevel(logging.INFO)
        logger.addHandler(handler)

    return log_file;