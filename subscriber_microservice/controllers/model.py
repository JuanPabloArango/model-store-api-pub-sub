"""Módulo que contiene los controladores para las vistas relacionadas con 'modelos'."""

# Librerías Externas.
from typing import Dict, List

from datetime import datetime

from flask_smorest import abort

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Librerías Internas.
from db import db
from models import ModelModel


class ModelController:
    """Clase que encapsula los controladores de modelos."""

    @staticmethod
    def get_all_models() -> List[ModelModel]:
        """Método que contiene el controlador para obtener todos los modelos.
        
        Returns:
        ----------
        List[ModelModel].
            Lista que contiene todos los registros."""

        problems = ModelModel.query.all()
        return problems
    
    @staticmethod
    def post_model(problem_id: str, model_data: Dict[str, str]) -> ModelModel:
        """Método que contiene el controlador para crear un modelo.
        
        Args:
        ----------
        problem_data: Dict[str, str].
            Request validada por un esquema.
        
        Returns:
        ----------
        ModelModel.
            Registro creado en la base de datos."""
        
        model = ModelModel(problem_id = problem_id, **model_data)

        try:
            db.session.add(model)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "Este modelo ya existe en la base de datos.")
        except SQLAlchemyError:
            abort(500, message = "Error al tratar de registrar el modelo.")

        return model
    
    @staticmethod
    def get_model(problem_id: str, model_id: str) -> ModelModel:
        """Método que contiene el controlador para obtener un modelo.
        
        Args:
        ----------
        problem_id: str.
            ID del problema a buscar en la base de datos.
        
        model_id: str.
            ID del modelo a buscar en la base de datos.
        
        Returns:
        ----------
        ModelModel.
            Registro de la base de datos."""
        
        model = ModelModel.query.filter(ModelModel.id == model_id, ModelModel.problem_id == problem_id).first()

        if model:
            return model
        return {"message": f"No existe un registro para el modelo {model_id} asociado al problema {problem_id}."}

    @staticmethod
    def delete_model(problem_id: str, model_id: str) -> ModelModel:
        """Método que contiene el controlador para eliminar un modelo.
        
        Args:
        ----------
        problem_id: str.
            ID del problema a buscar en la base de datos.
        
        model_id: str.
            ID del modelo a buscar en la base de datos.
        
        Returns:
        ----------
        ModelModel.
            Registro de la base de datos."""
        
        model = ModelModel.query.get_or_404(model_id)

        try:
            db.session.delete(model)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "Ocurrión un error al tratar de eliminar el registro.")
        
        return {"message": "Modelo eliminado."}
    
    @staticmethod
    def update_problem(problem_id: str, model_data: Dict[str, str]) -> ModelModel:
        """Método que contiene el controlador para actualizar un problema.
        
        Args:
        ----------
        problem_id: str.
            ID del problema a buscar en la base de datos.
        
        model_id: str.
            ID del modelo a buscar en la base de datos.
        
        Returns:
        ----------
        ProblemModel.
            Registro actualizado en la base de datos."""

        model = ModelModel.query.get_or_404(problem_id)

        for key, value in model_data.items():
            if hasattr(model, key):
                setattr(model, key, value)
        
        model.updated_at = datetime.now()
        
        db.session.add(model)
        db.session.commit()

        return model
