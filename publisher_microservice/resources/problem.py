"""Módulo que contiene las vistas 'problemas'."""

# Librerías Externas.
from typing import Dict

from flask import Response, request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

# Librerías Internas.
from workers.publisher import publish_msg, structure_msg

from schemas import PlainProblemSchema, UpdateProblemSchema, MessageSchema


blp = Blueprint("problem", __name__, description = "Vistas relacionadas con 'problemas'.")


@blp.route("/problem")
class ProblemList(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""

    #@blp.response(200, PlainProblemSchema(many = True))
    def get(self) -> Response:
        """Método GET que permite enviar a un servicio un requests y que este
        nos devuelva todos los problemas registrados.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente gracias a la información suministrada
            por el servicio."""

        # Debemos enviar un GET request a la API 2 (conectada a CloudSQL).

        pass
    
    #@jwt_required()
    @blp.arguments(PlainProblemSchema)
    def post(self, problem_data: Dict[str, str]) -> Response:
        """Método POST que permite enviar a Pub/Sub la información para crear
        un problema.

        Args:
        ----------
        problem_data: Dict[str, str].
            Data validada por marshmallow para crear problemas.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente para que sepa que la petición fue enviada."""
        
        pub_sub_msg = structure_msg(request_data = problem_data, request_ids = None, 
                                    table_name = "problems", action = "POST")

        publish_msg(pub_sub_msg)
        
        return jsonify({"status": "Mensaje enviado a Pub/Sub para crear problema."}), 200


@blp.route("/problem/<string:problem_id>")
class Problem(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""

    def get(self, problem_id: str) -> Response:
        """Método GET que permite enviar a un servicio un requests y que este
        nos devuelva el problema solicitado.
        
        Args:
        ----------
        problem_id: str.
            ID del problema a consultar.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
                
        # Debemos enviar un GET request a la API 2 (conectada a CloudSQL).

        pass

    @blp.arguments(UpdateProblemSchema)
    def put(self, problem_data: Dict[str, str], problem_id: str) -> Response:
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
                
        pub_sub_msg = structure_msg(request_data = problem_data, 
                                    request_ids = {"problem_id": problem_id}, 
                                    table_name = "problems", action = "PUT")

        publish_msg(pub_sub_msg)
        
        return jsonify({"status": "Mensaje enviado a Pub/Sub para actualizar problema."}), 200

    def delete(self, problem_id: str) -> Response:
        """Método DELETE que permite eliminar problema particular.
        
        Args:
        ----------
        problem_id: str.
            ID del problema a eliminar.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
        

        pub_sub_msg = structure_msg(request_data = None, 
                                    request_ids = {"problem_id": problem_id}, 
                                    table_name = "problems", action = "DELETE")

        publish_msg(pub_sub_msg)
        
        return jsonify({"status": "Mensaje enviado a Pub/Sub para eliminar problema."}), 200
