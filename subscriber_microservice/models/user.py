"""Módulo que contiene los modelos para las vistas relacionadas con 'users'."""

# Librerías Internas.
from db import db


class UserModel(db.Model):
    """Clase que contiene el modelo para los modelos."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True, 
                   comment = "Primary key de la tabla.")
    
    username = db.Column(db.String(20), unique = True, nullable = False, 
                         comment = "Nombre del usuario.")
    
    password = db.Column(db.String(1000), unique = False, nullable = False, 
                         comment = "Contraseña del usuario.")
