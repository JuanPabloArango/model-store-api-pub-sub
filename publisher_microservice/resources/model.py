"""Módulo que contiene las vistas 'modelos'."""

# Librerías Externas.
from typing import Dict

from flask import Response, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

# Librerías Internas.
from workers.publisher import publish_msg, structure_msg
from schemas import PlainModelSchema, UpdateModelSchema, MessageSchema


blp = Blueprint("models", __name__, description = "Vistas relacionadas con 'modelos'.")


@blp.route("/model")
class ModelList(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""

    @blp.response(200, PlainModelSchema(many = True))
    def get(self) -> Response:
        """Método GET que permite listar todos los modelos.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""

        pass


@blp.route("/problem/<string:problem_id>/model")
class ModelCreation(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""
    
    #@jwt_required()
    @blp.arguments(PlainModelSchema)
    def post(self, model_data: Dict[str, str], problem_id: str) -> Response:
        """Método POST que permite crear un problema.

        Args:
        ----------
        model_data: Dict[str, str].
            Data validada por marshmallow para crear modelos.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
                
        pub_sub_msg = structure_msg(request_data = model_data, 
                                    request_ids = {"problem_id": problem_id}, 
                                    table_name = "models", action = "POST")

        publish_msg(pub_sub_msg)
        
        return jsonify({"status": "Mensaje enviado a Pub/Sub para crear modelo."}), 200


@blp.route("/problem/<string:problem_id>/model/<string:model_id>")
class Model(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""
    
    def get(self, problem_id: str, model_id: str) -> Response:
        """Método GET que permite obtener un modelo de un problema determinado.

        Args:
        ----------
        problem_id: str.
            ID del problema.
        
        model_id: str.
            ID del modelo.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
        
        pass
    
    def delete(self, problem_id: str, model_id: str) -> Response:
        """Método GET que permite obtener un modelo de un problema determinado.

        Args:
        ----------
        problem_id: str.
            ID del problema.
        
        model_id: str.
            ID del modelo.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
        
        pub_sub_msg = structure_msg(request_data = None, 
                                    request_ids = {"problem_id": problem_id, 
                                                   "model_id": model_id}, 
                                    table_name = "models", action = "DELETE")

        publish_msg(pub_sub_msg)
        
        return jsonify({"status": "Mensaje enviado a Pub/Sub para eliminar modelo."}), 200
    
    @blp.arguments(UpdateModelSchema)
    def put(self, model_data: Dict[str, str], problem_id: str, model_id: str) -> Response:
        """Método PUT que permite crear o actualizar un problema particular.
        
        Args:
        ----------
        problem_data: Dict[str, str].
            Datos para actualizar el registro.

        problem_id: str.
            ID del problema a actualizar o crear en caso de que no exista.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
                
        pub_sub_msg = structure_msg(request_data = model_data, 
                                    request_ids = {"problem_id": problem_id, 
                                                   "model_id": model_id}, 
                                    table_name = "models", action = "PUT")

        publish_msg(pub_sub_msg)
        
        return jsonify({"status": "Mensaje enviado a Pub/Sub para actualizar modelo."}), 200
