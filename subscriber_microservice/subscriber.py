"""Módulo encargado de las comunicaciones con Pub/Sub."""

# Librerías Externas.
import json

from google.cloud import pubsub_v1

# Librerías Internas.
from app import create_app
from handlers.message_handler import MessageHandler

from config import PROJECT_ID, SUBSCRIPTION_NAME


app = create_app()


subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(PROJECT_ID, SUBSCRIPTION_NAME)


def process_msg() -> None:
    """Función que encapsula la lógica de trabajo de qué hacer con los mensajes."""
    
    response = subscriber.pull(request = {"subscription": subscription_path, 
                                          "max_messages": 10})
    
    if not response.received_messages:
        print("No hay mensajes qué procesar aún.")
        return

    for received_message in response.received_messages:

        try:
            data = json.loads(received_message.message.data.decode("utf-8"))

            request_ids = data["ids"]
            metadata = data["metadata"]
            request_data = data["request"]

            with app.app_context():

                MessageHandler.process_message(request_data, request_ids, metadata)
                        
            subscriber.acknowledge(request={"subscription": subscription_path, 
                                            "ack_ids": [received_message.ack_id]})
            
            print(f"Mensaje procesado: {data}")

        except Exception as e:
            print(f"Error procesando el mensaje: {e}")


if __name__ == "__main__":
    process_msg()
