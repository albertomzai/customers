"""Backend package for the CRM application."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

def create_app(test_config=None):
    """Create and configure a new Flask application instance.

    Args:
        test_config (dict, optional): Configuration dictionary for testing.
    Returns:
        flask.Flask: The configured Flask application.
    """

    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Default configuration
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///clientes.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    if test_config:
        app.config.update(test_config)

    # Initialize extensions with the app
    db.init_app(app)

    # Register blueprints
    from .routes import clientes_bp
    app.register_blueprint(clientes_bp, url_prefix='/api/clientes')

    # Create database tables on first request
    @app.before_first_request
    def create_tables():
        db.create_all()

    # Root route to serve the frontend index.html
    @app.route('/')
    def root():
        return app.send_static_file('index.html')

    return app

# Create a global app instance for import by tests and run.py
app = create_app()