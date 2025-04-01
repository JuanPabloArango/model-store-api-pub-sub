"""Módulo que contiene los modelos para las vistas relacionadas con 'problemas'."""

# Librerías Externas.
from datetime import datetime

# Librerías Internas.
from db import db


class ProblemModel(db.Model):
    """Clase que contiene el modelo para los problemas."""

    __tablename__ = "problems"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True, 
                   comment = "Primary key de la tabla.")
    
    name = db.Column(db.String(100), unique = True, nullable = False,
                     comment = "Nombre del problema. Indica el nombre del problema identificado por el negocio.")
    
    type = db.Column(db.String(20), unique = False, nullable = False, 
                     comment = "Tipo de problema que se resuelve.")
    
    owner_team = db.Column(db.String(100), unique = False, nullable = False,
                           comment = "Equipo dueño del problema.")
    
    owner = db.Column(db.String(100), unique = False, nullable = False,
                      comment = "Persona dentro del equipo que se encarga del problema.")
    
    repository = db.Column(db.String(100), unique = False, nullable = False,
                           comment = "Repositorio destinado para trabajar el problema.")
    
    description = db.Column(db.Text, unique = False, nullable = False,
                           comment = "Breve explicación del problema.")
    
    documentation = db.Column(db.String(100), unique = True, nullable = False,
                              comment = "Link a la documentación del problema.")
    
    execution = db.Column(db.String(20), unique = False, nullable = False, 
                          comment = "Cómo se ejecutará la solución al problema.")
    
    created_at = db.Column(db.DateTime, unique = False, nullable=False, default = datetime.now(),
                           comment = "Cómo se ejecutará la solución al problema.")

    updated_at = db.Column(db.DateTime, unique = False, nullable=False, default = datetime.now(),
                           comment = "Cómo se ejecutará la solución al problema.")
    
    model = db.relationship("ModelModel", back_populates = "problem", lazy = "dynamic", cascade = "all, delete")
