"""Módulo que contiene las vistas 'users'."""

# Librerías Externas.
from typing import Dict

from flask import Response
from flask.views import MethodView
from flask_smorest import Blueprint

# Librerías Internas.
from schemas import PlainUserSchema, MessageSchema


blp = Blueprint("user", __name__, description = "Vistas relacionadas con 'usuarios'.")


@blp.route("/register")
class UserRegister(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""

    @blp.arguments(PlainUserSchema)
    def post(self, user_data: Dict[str, str]) -> Response:
        """Método POST encargado de crear usuarios.
        
        Args:
        ----------
        user_data: Dict[str, str].
            Request validado.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
        
        pass
    

@blp.route("/login")
class UserRegister(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""

    @blp.arguments(PlainUserSchema)
    def post(self, user_data: Dict[str, str]) -> Response:
        """Método POST encargado de registrar al usuario en la API.
        
        Args:
        ----------
        user_data: Dict[str, str].
            Request validado.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
        
        pass


@blp.route("/user/<string:user_id>")
class User(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""

    @blp.response(200, PlainUserSchema, description = "Usuario obtenido exitosamente.")
    def get(self, user_id: str) -> Response:
        """Método GET que nos permite obtener a un usuario.
        
        Args:
        ----------
        user_id: str.
            ID del usuario.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""

        pass

    @blp.response(202, MessageSchema, description = "Eliminación exitosa.")
    def delete(self, user_id: str) -> Response:
        """Método POST que nos permite obtener a un usuario.
        
        Args:
        ----------
        user_id: str.
            ID del usuario.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""

        pass
