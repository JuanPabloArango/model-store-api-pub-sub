"""Módulo que contiene diferentes esquemas."""

# Librerías Externas.
from typing import Dict

from marshmallow import Schema, fields, validate, post_load, validates, ValidationError


URL_REGEX = r"^(https?:\/\/)?([\w\-]+\.)+[\w\-]+(\/[\w\-._~:/?#[\]@!$&'()*+,;=]*)?$"


class MessageSchema(Schema):
    """Clase que contiene el esquema en caso de requerir enviar un mensaje al cliente."""

    message = fields.Str(dump_only = True)


class PlainProblemSchema(Schema):
    """Clase que contiene los esquemas de validación para 'problem'."""

    id = fields.Int(dump_only = True)
    
    name = fields.Str(required = True,
                      validate = validate.Length(min = 3, max = 100),
                      error_messages = {"invalid": "El nombre debe ser un string.",
                                        "required": "Es obligatorio definir un nombre para el problema.",
                                        "validator_failed": "La longitud del nombre debe estar entre 3 y 100 caracteres."})
    
    type = fields.Str(required = True,
                      validate = validate.OneOf(choices = ["regression", "classification", "clustering"],
                                                labels = ["REGRESSION", "CLASSIFICATION", "CLUSTERING"]),
                      error_messages = {"invalid": "El tipo debe ser un string.",
                                        "required": "Es obligatorio definir un tipo para el problema.",
                                        "validator_failed": "El tipo del problema debe ser ('regression', 'classification', 'clustering')."})
    
    owner_team = fields.Str(required = True,
                            validate = validate.Length(min = 3, max = 100),
                            error_messages = {"invalid": "El equipo debe ser un string.",
                                              "required": "Es obligatorio definir un equipo para el problema.",
                                              "validator_failed": "La longitud del nombre debe estar entre 3 y 100 caracteres."})
    
    owner = fields.Str(required = True,
                       validate = validate.Length(min = 3, max = 100),
                       error_messages = {"invalid": "El dueño debe ser un string.",
                                         "required": "Es obligatorio definir un dueño para el problema.",
                                         "validator_failed": "La longitud del dueño debe estar entre 3 y 100 caracteres."})
    
    repository = fields.Str(required = True,
                            validate = validate.Regexp(URL_REGEX,
                                                       error = "Formato URL inválido. Example: https://github.com"),
                            error_messages = {"invalid": "La URL debe ser un string.",
                                              "required": "Debe anexar una URL del repositorio para el problema.",
                                              "validator_failed": "Formato URL inválido. Example: https://github.com"})
    
    description = fields.Str(required = True,
                             validate = validate.Length(min = 3, max = 2000),
                             error_messages = {"invalid": "Debe definir una descripción válida para el problema.",
                                               "required": "Debe definir una descripción para el problema.",
                                               "validator_failed": "La longitud del dueño debe estar entre 3 y 2000 caracteres."})
    
    documentation = fields.Str(required = True,
                               validate = validate.Regexp(URL_REGEX,
                                                          error = "Formato URL inválido. Example: https://example.com"),
                               error_messages = {"invalid": "La URL debe ser un string.",
                                                 "required": "Debe anexar una URL donde documente el problema.",
                                                 "validator_failed": "Formato URL inválido. Example: https://example.com"})
    
    execution = fields.Str(required = True,
                           validate = validate.OneOf(choices = ["batch", "online"],
                                                     labels = ["BATCH", "ONLINE"]),
                           error_messages = {"invalid": "El tipo de ejecución debe ser un string.",
                                             "required": "Es obligatorio definir un tipo de ejecución para el problema.",
                                             "validator_failed": "El tipo del problema debe ser ('batch', 'online')."})
    
    created_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")

    updated_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")


class PlainModelSchema(Schema):
    """Clase que contiene los esquemas de validación para 'model'."""

    id = fields.Int(dump_only = True)

    problem_id = fields.Int(dump_only = True)

    frequency = fields.Str(required = True,
                           validate = validate.OneOf(choices = ["daily", "weekly", "monthly"],
                                                     labels = ["DAILY", "WEEKLY", "MONTHLY"]),
                           error_messages = {"invalid": "La frecuencia de ejecución debe ser un string.",
                                             "validator_failed": "La frecuencia de ejecución debe ser ('daily', 'weekly', 'monthly')."})
    
    days = fields.Str(required = True,
                     validate = validate.Length(min = 2, max = 2),
                     error_messages = {"invalid": "El día de ejecucón debe ser pasado como string.",
                                       "validator_failed": "El día de ejecución debe estar en formato '01'."})
    
    time = fields.Str(required = True,
                     validate = validate.Length(min = 5, max = 5),
                     error_messages = {"invalid": "La hora de ejecucón debe ser pasado como string.",
                                       "validator_failed": "La hora de ejecucón debe estar en formato '05:00'."})
    
    created_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")

    updated_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")


class PlainVersionSchema(Schema):
    """Clase que contiene los esquemas de validación para 'versions'."""

    id = fields.Int(dump_only = True)
    
    model_id = fields.Int(dump_only = True)
    
    version = fields.Str(required = True,
                         validate = validate.Length(min = 1, max = 2),
                         error_messages = {"invalid": "La versión debe ser pasada como string.",
                                           "validator_failed": "La versión del modelo debe ser mayor a 1 y menor a 99."})
    
    status = fields.Str(dump_only = True)
    
    metrics = fields.Raw(required = True)
    
    created_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")

    updated_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")
    
    semantic_version = fields.Str(dump_only = True)

    @validates("metrics")
    def validate_metrics_dict(self, metrics: Dict[str, float]) -> None:
        """Método que valida el campo 'metrics'."""

        if not isinstance(metrics, dict):
            raise ValidationError("Sus métricas deben ser pasadas como diccionario.")
        
        if len(metrics) < 2:
            raise ValidationError("Debe ingresar al menos la métrica en entrenamiento y validación.")

    @post_load
    def set_constant_value(self, data: Dict[str, str], **kwargs) -> Dict[str, str]:
        """Metodo que nos permite siempre settear el campo 'status' a 'DEV'.
        
        Args:
        ----------
        Dict[str, str].
            Request enviada por el usuario.
        
        Returns:
        ----------
        Dict[str, str].
            Request configurada."""
        
        data["status"] = "DEV"
        return data
    

class PlainUserSchema(Schema):
    """Clase que contiene los esquemas de validación para 'users'."""

    id = fields.Int(dump_only = True)

    username = fields.Str(required = True,
                          validate = validate.Length(min = 5, max = 20),
                          error_messages = {"invalid": "El nombre de usuario debe ser un string.",
                                            "validator_failed": "La longitud del nombre de usuario debe estar entre 5 y 20 caracteres."})
    
    password = fields.Str(required = True,
                          validate = validate.Length(min = 5, max = 20),
                          error_messages = {"invalid": "La contraseña debe ser un string.",
                                            "validator_failed": "La longitud de la contraseña debe estar entre 5 y 20 caracteres."})
    

class UpdateProblemSchema(Schema):
    """Clase que contiene los esquemas de validación para 'problem'."""

    id = fields.Int(dump_only = True)
    
    name = fields.Str(required = False,
                      validate = validate.Length(min = 3, max = 100),
                      error_messages = {"invalid": "El nombre debe ser un string.",
                                        "validator_failed": "La longitud del nombre debe estar entre 3 y 100 caracteres."})
    
    type = fields.Str(required = False,
                      validate = validate.OneOf(choices = ["regression", "classification", "clustering"],
                                                labels = ["REGRESSION", "CLASSIFICATION", "CLUSTERING"]),
                      error_messages = {"invalid": "El tipo debe ser un string.",
                                        "validator_failed": "El tipo del problema debe ser ('regression', 'classification', 'clustering')."})
    
    owner_team = fields.Str(required = False,
                            validate = validate.Length(min = 3, max = 100),
                            error_messages = {"invalid": "El equipo debe ser un string.",
                                              "validator_failed": "La longitud del nombre debe estar entre 3 y 100 caracteres."})
    
    owner = fields.Str(required = False,
                       validate = validate.Length(min = 3, max = 100),
                       error_messages = {"invalid": "El dueño debe ser un string.",
                                         "validator_failed": "La longitud del dueño debe estar entre 3 y 100 caracteres."})
    
    repository = fields.Str(required = False,
                            validate = validate.Regexp(URL_REGEX,
                                                       error = "Formato URL inválido. Example: https://github.com"),
                            error_messages = {"invalid": "La URL debe ser un string.",
                                              "validator_failed": "Formato URL inválido. Example: https://github.com"})
    
    description = fields.Str(required = False,
                             validate = validate.Length(min = 3, max = 2000),
                             error_messages = {"invalid": "Debe definir una descripción válida para el problema.",
                                               "validator_failed": "La longitud del dueño debe estar entre 3 y 2000 caracteres."})
    
    documentation = fields.Str(required = False,
                               validate = validate.Regexp(URL_REGEX,
                                                          error = "Formato URL inválido. Example: https://example.com"),
                               error_messages = {"invalid": "La URL debe ser un string.",
                                                 "validator_failed": "Formato URL inválido. Example: https://example.com"})
    
    execution = fields.Str(required = False,
                           validate = validate.OneOf(choices = ["batch", "online"],
                                                     labels = ["BATCH", "ONLINE"]),
                           error_messages = {"invalid": "El tipo de ejecución debe ser un string.",
                                             "validator_failed": "El tipo del problema debe ser ('batch', 'online')."})
    
    created_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")

    updated_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")


class UpdateModelSchema(Schema):
    """Clase que contiene los esquemas de validación para 'model'."""

    id = fields.Int(dump_only = True)

    problem_id = fields.Int(dump_only = True)

    frequency = fields.Str(required = False,
                           validate = validate.OneOf(choices = ["daily", "weekly", "monthly"],
                                                     labels = ["DAILY", "WEEKLY", "MONTHLY"]),
                           error_messages = {"invalid": "La frecuencia de ejecución debe ser un string.",
                                             "validator_failed": "La frecuencia de ejecución debe ser ('daily', 'weekly', 'monthly')."})
    
    days = fields.Str(required = False,
                     validate = validate.Length(min = 2, max = 2),
                     error_messages = {"invalid": "El día de ejecucón debe ser pasado como string.",
                                       "validator_failed": "El día de ejecución debe estar en formato '01'."})
    
    time = fields.Str(required = False,
                     validate = validate.Length(min = 5, max = 5),
                     error_messages = {"invalid": "La hora de ejecucón debe ser pasado como string.",
                                       "validator_failed": "La hora de ejecucón debe estar en formato '05:00'."})
    
    created_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")

    updated_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")


class UpdateVersionSchema(Schema):
    """Clase que contiene los esquemas de validación para 'version'."""

    id = fields.Int(dump_only = True)
    
    model_id = fields.Int(dump_only = True)
    
    version = fields.Str(required = False,
                         validate = validate.Length(min = 1, max = 2),
                         error_messages = {"invalid": "La versión debe ser pasada como string.",
                                           "validator_failed": "La versión del modelo debe ser mayor a 1 y menor a 99."})
    
    status = fields.Str(dump_only = True)
    
    metrics = fields.Raw(required = False)
    
    created_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")

    updated_at = fields.DateTime(dump_only = True, format = "%Y-%m-%d %H:%M:%S")
    
    semantic_version = fields.Str(dump_only = True)

    @validates("metrics")
    def validate_metrics_dict(self, metrics: Dict[str, float]) -> None:
        """Método que valida el campo 'metrics'."""

        if not isinstance(metrics, dict):
            raise ValidationError("Sus métricas deben ser pasadas como diccionario.")
        
        if len(metrics) < 2:
            raise ValidationError("Debe ingresar al menos la métrica en entrenamiento y validación.")
