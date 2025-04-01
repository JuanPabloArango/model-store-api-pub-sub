"""Módulo que contiene los controladores para las vistas relacionadas con 'problemas'."""

# Librerías Externas.
from typing import Dict, List

from datetime import datetime

from flask_smorest import abort

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# Librerías Internas.
from db import db
from models import ProblemModel


class ProblemController:
    """Clase que encapsula los controladores de problemas."""

    @staticmethod
    def get_all_problems() -> List[ProblemModel]:
        """Método que contiene el controlador para obtener todos los problemas.
        
        Returns:
        ----------
        List[ProblemModel].
            Lista que contiene todos los registros."""

        problems = ProblemModel.query.all()
        return problems
    
    @staticmethod
    def post_problem(problem_data: Dict[str, str]) -> ProblemModel:
        """Método que contiene el controlador para crear un problema.
        
        Args:
        ----------
        problem_data: Dict[str, str].
            Request validada por un esquema.
        
        Returns:
        ----------
        ProblemModel.
            Registro creado en la base de datos."""
        
        problem = ProblemModel(**problem_data)

        try:
            db.session.add(problem)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "Este problema ya existe en la base de datos.")
        except SQLAlchemyError:
            abort(500, message = "Error al tratar de registrar el problema.")

        return problem
    
    @staticmethod
    def get_problem(problem_id: int) -> ProblemModel:
        """Método que contiene el controlador para obtener un problema.
        
        Args:
        ----------
        problem_id: int.
            ID del problema a buscar en la base de datos.
        
        Returns:
        ----------
        ProblemModel.
            Registro de la base de datos."""
        
        problem = ProblemModel.query.get_or_404(problem_id)
        return problem
    
    @staticmethod
    def delete_problem(problem_id: int) -> Dict[str, str]:
        """Método que contiene el controlador para eliminar un problema.
        
        Args:
        ----------
        problem_id: int.
            ID del problema a buscar en la base de datos.
        
        Returns:
        ----------
        Dict[str, str].
            Mensaje de eliminación exitosa del problema."""
        
        problem = ProblemModel.query.get_or_404(problem_id)

        try:
            db.session.delete(problem)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "Ocurrión un error al tratar de eliminar el registro.")
        
        return {"message": "Problema eliminado."}
    
    @staticmethod
    def update_problem(problem_id: int, problem_data: Dict[str, str]) -> ProblemModel:
        """Método que contiene el controlador para actualizar un problema.
        
        Args:
        ----------
        problem_id: int.
            ID del problema a buscar en la base de datos.
        
        problem_data: Dict[str, str].
            Campos a actualizar sobre el registro.
        
        Returns:
        ----------
        ProblemModel.
            Registro actualizado en la base de datos."""

        problem = ProblemModel.query.get_or_404(problem_id)

        for key, value in problem_data.items():
            if hasattr(problem, key):
                setattr(problem, key, value)
        
        problem.updated_at = datetime.now()
        
        db.session.add(problem)
        db.session.commit()

        return problem
