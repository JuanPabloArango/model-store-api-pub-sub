"""Módulo que encapsula todas las funcionalidades de la app."""

# Librerías Externas.
from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate


# Librerías Internas.
import models
from db import db
from config import Config


def create_app() -> Flask:
    """Función que encapsula la creación de la app.
    
    Returns:
    ----------
    Flask.
        App."""
    
    app = Flask(__name__)

    app.json.sort_keys = False
    app.config.from_object(Config)

    db.init_app(app)

    api = Api(app)
    migrate = Migrate(app, db)

    @app.before_request
    def create_tables() -> None:
        """Función que crea las tablas definidas en nuestra app."""

        db.create_all()

    return app
