from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Instancia de la base de datos, se inicializará en create_app
db = SQLAlchemy()

def create_app():
    """Factory function to create and configure the Flask app."""
    app = Flask(__name__, static_folder='../frontend', static_url_path='')

    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializar extensiones
    db.init_app(app)

    # Registrar blueprints
    from .routes import clientes_bp
    app.register_blueprint(clientes_bp, url_prefix='/api')

    @app.route('/')
    def index():
        """Serve the frontend entry point."""
        return app.send_static_file('index.html')

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()

    return app