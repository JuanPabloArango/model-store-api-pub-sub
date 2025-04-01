"""Módulo que contiene los modelos para las vistas relacionadas con 'versiones'."""

# Librerías Externas.
from __future__ import annotations

from datetime import datetime

# Librerías Internas.
from db import db


class VersionModel(db.Model):
    """Clase que contiene el modelo para las versiones."""

    __tablename__ = "versions"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True, 
                   comment = "Primary key de la tabla.")
    
    model_id = db.Column(db.Integer, db.ForeignKey("models.id"), unique = False, nullable = False,
                         comment = "Foreign key de la tabla 'models'.")
    
    version = db.Column(db.String(3), unique = False, nullable = False,
                        comment = "Versión en la que va el modelo.")
    
    status = db.Column(db.String(20), unique = False, nullable = False, default = "DEV",
                       comment = "Estado de la versión.")
    
    metrics = db.Column(db.JSON, unique = False, nullable = False, 
                     comment = "Métricas de la versión.")
    
    created_at = db.Column(db.DateTime, unique = False, nullable=False, default = datetime.now(),
                           comment = "Cómo se ejecutará la solución al problema.")

    updated_at = db.Column(db.DateTime, unique = False, nullable=False, default = datetime.now(),
                           comment = "Cómo se ejecutará la solución al problema.")
    
    semantic_version = db.Column(db.String(100), unique = False, nullable = False,
                                 comment = "Versión semántica del modelo.")
    
    model = db.relationship("ModelModel", back_populates = "version")

    def clone(self, **kwargs) -> VersionModel:
        """Método que permite clonar una versión para 
        sacar una nueva versión en base a esta.
        
        Returns:
        ----------
        VersionModel.
            Nueva versión."""

        new_data = {col.name: getattr(self, col.name) for col in self.__table__.columns if col.name not in ("id")}
        new_data.update(kwargs)

        return VersionModel(**new_data)
