from flask import Flask, redirect, send_from_directory
from flasgger import Swagger
from flask_talisman import Talisman
from dotenv import load_dotenv
import logging
import os

from controllers.student_controller import student_bp

# Load environment variables from .env file
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load configuration from external file
app.config.from_pyfile('config.py')

# Relaxed CSP to allow Swagger UI to load properly
csp = {
    'default-src': [
        '\'self\'',
        'https://cdnjs.cloudflare.com',
        'https://cdn.jsdelivr.net'
    ],
    'script-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'https://cdnjs.cloudflare.com',
        'https://cdn.jsdelivr.net'
    ],
    'style-src': [
        '\'self\'',
        '\'unsafe-inline\'',
        'https://cdnjs.cloudflare.com',
        'https://cdn.jsdelivr.net'
    ]
}

# Apply security headers with relaxed CSP
Talisman(app, content_security_policy=csp)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.info("Starting the Flask application...")

# Swagger template and config
swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Student API",
        "version": "1.0",
        "description": "API documentation for student management",
    },
    "basePath": "/",
}

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "uiversion": 3
}

swagger = Swagger(app, template=swagger_template, config=swagger_config)

# Register Blueprints
app.register_blueprint(student_bp, url_prefix='/api/students')

# Optional: Redirect root to Swagger UI
@app.route('/')
def redirect_to_swagger():
    return redirect('/apidocs/')

# Serve favicon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon-32x32.png',
        mimetype='image/png'
    )

# Global error handler
@app.errorhandler(Exception)
def handle_exception(e):
    logger.exception("Unhandled exception occurred:")
    return {"error": str(e)}, 500

# Run the app
if __name__ == '__main__':
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode)
