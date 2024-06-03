from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

from app import models, routes

# Load the cloud environment data
import sys
from app.cloud_env import load_cloud_env

if len(sys.argv) > 1:
    input_file = sys.argv[1]
    with app.app_context():
        load_cloud_env(f'inputs/{input_file}')
else:
    print("Please provide the input file as an argument.")
    print("Example: python app.py input-2.json")
    sys.exit(1)