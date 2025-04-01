"""Módulo que contiene los modelos para las vistas relacionadas con 'modelos'."""

# Librerías Externas.
from datetime import datetime

# Librerías Internas.
from db import db


class ModelModel(db.Model):
    """Clase que contiene el modelo para los modelos."""

    __tablename__ = "models"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True, 
                   comment = "Primary key de la tabla.")
    
    problem_id = db.Column(db.Integer, db.ForeignKey("problems.id"), unique = True, nullable = False,
                           comment = "Foreign key de la tabla 'problems'.")
    
    frequency = db.Column(db.String(20), unique = False, nullable = False, 
                          comment = "Frecuencia de ejecución del modelo.")
    
    days = db.Column(db.String(2), unique = False, nullable = False, 
                     comment = "Día de ejecución del modelo. Si la frecuencia es mensual, lleva el día del mes. \
                                Si la frecuencia es semanal, va el día de la semana (lunes = 1, domingo = 7). \
                                Si la frecuencia es diaria, va 'all'.")
    
    time = db.Column(db.String(5), unique = False, nullable = False,
                     comment = "Hora de ejecución del modelo.")
    
    created_at = db.Column(db.DateTime, unique = False, nullable=False, default = datetime.now(),
                           comment = "Cómo se ejecutará la solución al problema.")

    updated_at = db.Column(db.DateTime, unique = False, nullable=False, default = datetime.now(),
                           comment = "Cómo se ejecutará la solución al problema.")

    problem = db.relationship("ProblemModel", back_populates = "model")

    version = db.relationship("VersionModel", back_populates = "model", lazy = "dynamic", cascade = "all, delete")
    