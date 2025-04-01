"""Módulo que contiene los controladores para las vistas relacionadas con 'usuarios'."""

# Librerías Externas.
from typing import Dict

from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token

from flask_smorest import abort

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Librerías Internas.
from db import db
from models import UserModel


class UserController:
    """Clase que encapsula los controladores de problemas."""

    @staticmethod
    def post_user(user_data: Dict[str, str]) -> UserModel:
        """Controlador encargado de manejar la creación de usuarios.
        
        Args:
        ----------
        user_data: Dict[str, str].
            Información del usuario a crear.

        Returns:
        ----------
        UserModel.
            Usuario creado."""
        
        user = UserModel(username = user_data["username"], password = pbkdf2_sha256.hash(user_data["password"]))
        
        try:
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "Este usuario ya existe en la base.")
        except SQLAlchemyError:
            abort(500, message = "No ha sido posible crear el usuario.")
        
        return {"message": "Usuario creado exitosamente."}
    
    @staticmethod
    def get_user(user_id: int) -> UserModel:
        """Controlador encargado de manejar la obtención de usuarios.
        
        Args:
        ----------
        user_id: int
            ID del usuario a obtener.

        Returns:
        ----------
        UserModel.
            Usuario creado."""
        
        user = UserModel.query.get_or_404(user_id)
        return user
    
    @staticmethod
    def delete_user(user_id: int) -> UserModel:
        """Controlador encargado de manejar la eliminación de usuarios.
        
        Args:
        ----------
        user_id: int
            ID del usuario a eliminar.

        Returns:
        ----------
        UserModel.
            Usuario creado."""
        
        user = UserModel.query.get_or_404(user_id)

        try:
            db.session.delete(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "Hubo un error al tratar de eliminar el usuario.")

        return {"message": "Usuario eliminado."}
    
    @staticmethod
    def login(user_data: Dict[str, str]) -> UserModel:
        """Controlador encargado de manejar el registro de usuarios.
        
        Args:
        ----------
        user_data: Dict[str, str].
            Información del usuario a crear.

        Returns:
        ----------
        UserModel.
            Usuario creado."""
        
        user = UserModel.query.filter(UserModel.username == user_data["username"]).first()

        if user and pbkdf2_sha256.verify(user_data["password"], user.password):

            access_token = create_access_token(identity = str(user.id))
            return {"access_token": access_token}
        
        abort(401, message = "Credenciales inválidas.")
