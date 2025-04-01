"""Módulo que contiene las vistas 'versiones'."""

# Librerías Externas.
from typing import Dict

from flask import Response, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from flask_jwt_extended import jwt_required

# Librerías Internas.
from workers.publisher import publish_msg, structure_msg
from schemas import PlainVersionSchema, UpdateVersionSchema, MessageSchema


blp = Blueprint("versions", __name__, description = "Vistas relacionadas con 'versions'.")


@blp.route("/version")
class VersionList(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""

    def get(self) -> Response:
        """Método GET que permite consultar a un microservicio todas las versiones.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente por el microservicio."""

        # Debemos enviar un requests a la API 2 con la información de IDs.

        pass


@blp.route("/model/<string:model_id>/version")
class VersionCreation(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""
    
    #@jwt_required()
    @blp.arguments(PlainVersionSchema)
    def post(self, version_data: Dict[str, str], model_id: str) -> Response:
        """Método POST que permite crear un problema.

        Args:
        ----------
        version_data: Dict[str, str].
            Data validada por marshmallow para crear versión.
        
        model_id: str.
            ID del modelo para el cual se creará la versión.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
        
        pub_sub_msg = structure_msg(request_data = version_data, request_ids = {"model_id": model_id}, 
                                    table_name = "versions", action = "POST")

        publish_msg(pub_sub_msg)
        
        return jsonify({"status": "Mensaje enviado a Pub/Sub para crear versión."}), 200
    

@blp.route("/version/<string:version_id>/promote")
class VersionPromotion(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""

    @jwt_required()
    def post(self, version_id: str) -> Response:
        """Método POST que permite la promoción de un modelo a PROD.
        
        Args:
        ----------
        version_id: str.
            ID de la versión a promover.
            
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
        
        pass
    

@blp.route("/version/<string:version_id>/deprecate")
class VersionDeprecation(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""

    @jwt_required()
    def post(self, version_id: str) -> Response:
        """Método POST que permite la promoción de un modelo a PROD.
        
        Args:
        ----------
        version_id: str.
            ID de la versión a promover.
            
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
        
        pass

@blp.route("/model/<string:model_id>/version/<string:version_id>")
class Model(MethodView):
    """Clase que encapsula los verbos de la ruta definida."""
    
    def get(self, model_id: str, version_id: str) -> Response:
        """Método GET que permite obtener un modelo de un problema determinado.

        Args:
        ----------
        model_id: str.
            ID del modelo.
        
        version_id: str.
            ID de la versión.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
        
        pass
    
    def delete(self, model_id: str, version_id: str) -> Response:
        """Método GET que permite obtener un modelo de un problema determinado.

        Args:
        ----------
        model_id: str.
            ID del modelo.
        
        version_id: str.
            ID de la versión.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
        
        pub_sub_msg = structure_msg(request_data = None, 
                                    request_ids = {"model_id": model_id, 
                                                   "version_id": version_id}, 
                                    table_name = "versions", action = "DELETE")

        publish_msg(pub_sub_msg)
        
        return jsonify({"status": "Mensaje enviado a Pub/Sub para eliminar versión."}), 200
    
    @blp.arguments(UpdateVersionSchema)
    def put(self, version_data: Dict[str, str], model_id: str, version_id: str) -> Response:
        """Método PUT que permite crear o actualizar un problema particular.
        
        Args:
        ----------
        version_data: Dict[str, str].
            Datos para actualizar el registro.

        model_id: str.
            ID del modelo.
        
        version_id: str.
            ID de la versión.
        
        Returns:
        ----------
        Response.
            Respuesta enviada al cliente."""
                
        pub_sub_msg = structure_msg(request_data = version_data, 
                                    request_ids = {"model_id": model_id, 
                                                   "version_id": version_id}, 
                                    table_name = "versions", action = "PUT")

        publish_msg(pub_sub_msg)
        
        return jsonify({"status": "Mensaje enviado a Pub/Sub para actualizar versión."}), 200
