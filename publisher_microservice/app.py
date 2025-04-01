"""Módulo que encapsula todas las funcionalidades de la app."""

# Librerías Externas.
from typing import Dict

from flask_smorest import Api
from flask_jwt_extended import JWTManager
from flask import Flask, jsonify, Response


# Librerías Internas.
from config import Config

from resources import UserBlueprint
from resources import ModelBlueprint
from resources import ProblemBlueprint
from resources import VersionBlueprint


def create_app() -> Flask:
    """Función que encapsula la creación de la app.
    
    Returns:
    ----------
    Flask.
        App."""
    
    app = Flask(__name__)

    app.json.sort_keys = False
    app.config.from_object(Config)

    api = Api(app)
    jwt = JWTManager(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header: Dict[str, str], jwt_payload: Dict[str, str]) -> Response:
        """Función que protege a nuestros endpoints cuando ha pasado mucho tiempo
        desde el login.

        Args:
        ----------
        jwt_header: Dict[str, str]
            Información de los headers.

        jwt_payload: Dict[str, str].
            Información del request.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""

        return jsonify({"message": "El token ha expirado.",
                        "error": "Token expirado."}), 401
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error: str) -> Response:
        """Función que protege a nuestros endpoints de tokens inválidos.

        Args:
        ----------
        error: str.
            Error.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""

        return jsonify({"message": "El token es inválido.",
                        "error": "Token inválido."}), 401
    
    @jwt.unauthorized_loader
    def missing_token_callback(error: str) -> Response:
        """Función que protege a nuestros endpoints cuando no se envía el token.

        Args:
        ----------
        error: str.
            Error.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""

        return jsonify({"message": "No se ha pasado un token de autenticación.",
                        "error": "Se requiere un token de autenticación."}), 401

    api.register_blueprint(UserBlueprint)
    api.register_blueprint(ModelBlueprint)
    api.register_blueprint(ProblemBlueprint)
    api.register_blueprint(VersionBlueprint)

    return app
