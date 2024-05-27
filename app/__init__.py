import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask

app = Flask(__name__)

# Configure logging
log_file = os.path.join(app.root_path, 'app.log')
log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

file_handler = RotatingFileHandler(log_file, maxBytes=10240, backupCount=10)
file_handler.setFormatter(log_formatter)
file_handler.setLevel(logging.INFO)

app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

# Import routes and other components after initializing the app
from app import routes