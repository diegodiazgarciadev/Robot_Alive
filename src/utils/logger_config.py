# logger_config.py
import logging
import os
from logging.handlers import RotatingFileHandler

# Create the logs directory if it does not exist
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

# Basic logging configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# RotatingFileHandler configuration
handler = RotatingFileHandler(
    os.path.join(log_directory, 'app.log'), maxBytes=5000000, backupCount=5)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                              datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)

# Add the handler to the root logger
logging.getLogger('').addHandler(handler)
