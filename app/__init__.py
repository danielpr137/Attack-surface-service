from flask import Flask
import os
import json
import logging
from dotenv import load_dotenv
from app.db import db  # Import the db instance

def create_app():
    load_dotenv()
    app = Flask(__name__)

    # Set up logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    input_file = os.getenv('CLOUD_ENV_FILE')
    if not input_file:
        logger.error("CLOUD_ENV_FILE environment variable not set")
        raise RuntimeError("CLOUD_ENV_FILE environment variable not set")

    try:
        with open(input_file) as f:
            cloud_env = json.load(f)
            app.config['cloud_env'] = cloud_env
            app.config['vm_count'] = len(cloud_env['vms'])
            logger.info(f"Loaded cloud environment from {input_file}")
    except Exception as e:
        logger.error(f"Failed to load the cloud environment file: {e}")
        raise RuntimeError(f"Failed to load the cloud environment file: {e}")

    from app.routes import api_bp
    app.register_blueprint(api_bp, url_prefix='/api/v1')

    return app
