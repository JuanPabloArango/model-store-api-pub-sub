"""Módulo encargado de las comunicaciones con Pub/Sub."""

# Librerías Externas.
from typing import Dict, Optional

import json
from datetime import datetime

from google.cloud import pubsub_v1

# Librerías Internas.
from config import PROJECT_ID, TOPIC_NAME


publisher = pubsub_v1.PublisherClient()
topic_path = publisher.topic_path(PROJECT_ID, TOPIC_NAME)


def publish_msg(data: Dict[str, str]) -> None:
    """Función encargada de publicar mensajes en Pub/Sub.
    
    Args:
    ----------
    data: Dict[str, str].
        Data a publicar en el tópico de Pub/Sub."""
        
    encoded_msg = json.dumps(data).encode("utf-8")
    
    future = publisher.publish(topic_path, encoded_msg)
    msg_id = future.result()

def structure_msg(table_name: str, action: str,
                  request_data: Optional[Dict[str, str]] = None,
                  request_ids: Optional[Dict[str, int]] = None) -> Dict[str, str]:
    """Función auxiliar que permite definir la estructura de los mensajes
    a publicar en Pub/Sub.
    
    Args:
    ----------
    table_name: str.
        Tabla a impactar.

    action: str.
        Tipo de acción a realizar sobre la tabla objetivo.

    request_data: Optional[Dict[str, str]].
        Información enviada por el usuario.
    
    request_ids: Optional[Dict[str, int]].
        Información adicional relacionada con registros en la misma u otra tabla.
    
    Returns:
    ----------
    Dict[str, str].
        Información estructurada enviada a Pub/Sub."""

    msg_structure = {"request": request_data,
                     "ids": request_ids,
                     "metadata": {"table": table_name,
                                  "action": action, 
                                  "timestamp": datetime.utcnow().isoformat()}}
    
    return msg_structure