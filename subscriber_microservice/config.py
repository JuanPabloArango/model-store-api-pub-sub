"""Módulo que contiene las configuraciones de la app."""

# Librerías Externas.
import os

from dotenv import load_dotenv
load_dotenv()


PROJECT_ID = os.getenv("PROJECT_ID")
TOPIC_NAME = os.getenv("TOPIC_NAME")


class Config:
    """Clase que encapsula las configuraciones."""

    API_TITLE = "My Model Store"
    API_VERSION = "v1"

    PROPAGATE_EXCEPTIONS = True

    JWT_SECRET_KEY = "juan" ### Tratemos de usar secrets de GCP.
    
    OPENAPI_VERSION = "3.0.3"
    OPENAPI_URL_PREFIX = "/"
    OPENAPI_SWAGGER_UI_PATH = "/swagger-ui"
    OPENAPI_SWAGGER_UI_URL = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

    # Una vez cree la instancia de CloudSQL debe proceder a crear una base de datos y un usuario. 
    # También, debe configurar la instancia de CloudSQL para que reciba tráfico desde nuestra IP pública.
    # Una vez tenga la IP configurada en CloudSQL y haya creado una base de datos y un usuario,
    # llenará SQLALCHEMY_DATABASE_URI con nombre de usuario creado, contraseña creada para el usuario,
    # no para la instancia, sino para el usuario, debe obtener la IP pública de su instancia de Cloud SQL
    # y, por último, indicar el nombre de la base de datos creada, no de la instancia de CloudSQL.
    # Podra ver esto en el archivo .env en la variable LOCAL_DATABASE_URL. La variable DATABASE_URL
    # contiene el string para conexiones entre Cloud Run y Cloud SQL.

    # Ahora, ya que probamos nuestra instancia de CloudSQL en modo local, desplegamos la API en
    # Cloud Run.
    # Para hacer esto, no debe hacer nada en CloudSQL, pero sí en la configuración de su Cloud Run
    # y de su proyecto de GCP.

    # 1. Permita este permiso: gcloud services enable sqladmin.googleapis.com.
    # 2. Obtenga la cuenta de servicios con las que está desplegando APIs en Cloud Run mediante el comando:
         
    #    gcloud run services describe <cloud-run-project-name> --region <cloud-run-region> \
    #           --format="value(spec.template.spec.serviceAccountName)"

    #    Una vez obtenga la cuenta de servicios a la que necesita suministrar el permiso hará lo siguiente:

    #    gcloud projects add-iam-policy-binding <cloud-run-project-name> \
    #           --member="<cuenta-de-servicio-hallada-con-el-comando>" \
    #           --role="roles/cloudsql.client"

    # 3. En su configuración de Clour Run añada --add-cloudsql-instances YOUR_PROJECT_ID:YOUR_REGION:YOUR_INSTANCE_NAME (Esto lo puede hallar en la pestaña 'conexiones' de CloudSQL).

    # Con estos simples tres pasos, su API en la nube se debe conectar a CloudSQL.
