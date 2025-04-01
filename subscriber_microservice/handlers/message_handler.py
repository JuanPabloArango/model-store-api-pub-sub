"""Módulo que contiene la forma de procesar un mensaje de Pub/Sub."""

# Librerías Externas.
from typing import Dict

# Librerías Internas.
from controllers import ProblemController, ModelController, VersionController


class MessageHandler:
    """Clase que encapsula la lógica de procesamiento de un mensaje."""

    ACTIONS = {"problems": {"POST": ProblemController.post_problem,
                            "PUT": ProblemController.update_problem,
                            "DELETE": ProblemController.delete_problem},
               "models": {"POST": ModelController.post_model,
                          "PUT": ModelController.update_problem,
                          "DELETE": ModelController.delete_model},
               "versions": {"POST": VersionController.post_version,
                            "PUT": VersionController.update_version,
                            "DELETE": VersionController.delete_version}}
    
    @classmethod
    def process_message(cls, request_data: Dict[str, str], request_ids: Dict[str, int], metadata: Dict[str, str]):
        """Método de clase que procesa el mensaje para saber qué lógica seguir.
        
        Args:
        ----------
        request_data: Dict[str, str].
            Diccionario que contiene información que el usuario suministró.

        request_ids: Dict[str, int].
            Diccionario que contiene los registros puntuales a afectar.
        
        metadata: Dict[str, str].
            Metadata para entender el contexto del mensaje."""
        
        table = metadata.get("table", None)
        action = metadata.get("action", None)

        if table not in cls.ACTIONS:
            raise ValueError(f"No tenemos registrada la tabla '{table}'.")

        if action not in cls.ACTIONS[table]:
            raise ValueError(f"La tabla '{table}' solo maneja los verbos 'POST', 'PUT' y 'DELETE'.")

        handler_func = cls.ACTIONS[table][action]

        if table == "problem":
            return handler_func(problem_data = request_data, 
                                problem_id = request_ids["problem_id"])

        elif table == "models":
            return handler_func(model_data = request_data, 
                                problem_id = request_ids["problem_id"], 
                                model_id = request_ids["model_id"])

        else:
            return handler_func(version_data = request_data)
