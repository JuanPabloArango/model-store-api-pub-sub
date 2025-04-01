"""Módulo que contiene los controladores para las vistas relacionadas con 'versiones'."""

# Librerías Externas.
from typing import Dict, List

from datetime import datetime

from flask_smorest import abort

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Librerías Internas.
from db import db
from models import VersionModel


class VersionController:
    """Clase que encapsula los controladores de versión."""

    @staticmethod
    def get_all_versions() -> List[VersionModel]:
        """Método que contiene el controlador para obtener todas las versiones.
        
        Returns:
        ----------
        List[VersionModel].
            Lista que contiene todos los registros."""

        versions = VersionModel.query.all()
        return versions
    
    @staticmethod
    def post_version(model_id: int, version_data: Dict[str, str]) -> VersionModel:
        """Método que contiene el controlador para crear una versión.
        
        Args:
        ----------
        model_id: int.
            ID del modelo al cual se asocia la versión.

        version_data: Dict[str, str].
            Request validada por un esquema.
        
        Returns:
        ----------
        VersionModel.
            Registro creado en la base de datos."""
        
        version = VersionModel.query.filter(VersionModel.model_id == model_id, 
                                            VersionModel.version == version_data["version"]).order_by(VersionModel.semantic_version.desc()).first()
        
        if version:
            newest = int(version.semantic_version[-1]) + 1
            sem_version = version_data["version"] + f".0.0-dev-{str(newest)}"
        else:
            sem_version = version_data["version"] + ".0.0-dev-1"

        version = VersionModel(model_id = model_id, **version_data, semantic_version = sem_version)

        try:
            db.session.add(version)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "Esta versión ya existe en la base de datos.")
        except SQLAlchemyError:
            abort(500, message = "Error al tratar de registrar la versión.")

        return version
    
    @staticmethod
    def get_version(version_id: int) -> VersionModel:
        """Método que contiene el controlador para obtener una versión.
        
        Args:
        ----------
        version_id: int.
            ID de la versión a buscar en la base de datos.
        
        Returns:
        ----------
        VersionModel.
            Registro de la base de datos."""
        
        version = VersionModel.query.get_or_404(version_id)
        print(version)
        return version
    
    @staticmethod
    def delete_version(version_id: int) -> Dict[str, str]:
        """Método que contiene el controlador para eliminar una versión.
        
        Args:
        ----------
        version_id: int.
            ID de la versión a buscar en la base de datos.
        
        Returns:
        ----------
        Dict[str, str].
            Mensaje de eliminación exitosa de la versión."""
        
        version = VersionModel.query.get_or_404(version_id)

        try:
            db.session.delete(version)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "Ocurrión un error al tratar de eliminar el registro.")
        
        return {"message": "Versión eliminado."}
    
    @staticmethod
    def update_version(version_id: int, version_data: Dict[str, str]) -> VersionModel:
        """Método que contiene el controlador para actualizar una versión.
        
        Args:
        ----------
        version_id: int.
            ID de la versión a buscar en la base de datos.
        
        version_data: Dict[str, str].
            Campos a actualizar sobre el registro.
        
        Returns:
        ----------
        VersionModel.
            Registro actualizado en la base de datos."""

        version = VersionModel.query.get_or_404(version_id)

        for key, value in version_data.items():
            if hasattr(version, key):
                setattr(version, key, value)
        
        version.updated_at = datetime.now()
        
        db.session.add(version)
        db.session.commit()

        return version
    
    @staticmethod
    def promote_version(version_id: int) -> VersionModel:
        """Método que contiene el controlador para promover una versión.
        
        Args:
        ----------
        version_id: int.
            ID de la versión a buscar en la base de datos.

        Returns:
        ----------
        VersionModel.
            Registro actualizado en la base de datos."""
        
        version = VersionModel.query.get_or_404(version_id)

        version.status = "DEPRECATED"
        version.updated_at = datetime.now()

        new_status = "PROD"
        new_created_at = datetime.now()
        new_semantic_version = version.semantic_version.split("-")[0]

        new_version = version.clone(status = new_status, 
                                    created_at = new_created_at,
                                    semantic_version = new_semantic_version)

        try:
            db.session.add(version)
            db.session.add(new_version)

            db.session.commit()

        except SQLAlchemyError:
                abort(500, message = "Error al tratar de promover la versión.")

        return {"message": f"La version {version.id} fue deprecada debido a la promoción hacia producción en su versión {new_version.id}."}

    @staticmethod
    def deprecate_version(version_id: int) -> VersionModel:
        """Método que contiene el controlador para promover una versión.
        
        Args:
        ----------
        version_id: int.
            ID de la versión a buscar en la base de datos.

        Returns:
        ----------
        VersionModel.
            Registro actualizado en la base de datos."""
        
        version = VersionModel.query.get_or_404(version_id)

        version.status = "DEPRECATED"
        version.updated_at = datetime.now()

        try:
            db.session.add(version)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "Error al tratar de deprecar la versión.")

        return {"message": f"La version {version.id} fue deprecada."}
