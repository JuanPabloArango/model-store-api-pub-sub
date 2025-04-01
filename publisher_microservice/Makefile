docker_build_api:
	docker build -f Dockerfile -t us-east1-docker.pkg.dev/<PROJECT_ID>/<IMAGES_FOLDER>/<IMAGE_NAME> . --platform linux/amd64/v2

docker_push_api:
	docker push us-east1-docker.pkg.dev/<PROJECT_ID>/<IMAGES_FOLDER>/<IMAGE_NAME>:latest

deploy_cloud_run_pruebas:
	gcloud run deploy <CLOUD_RUN_NAME> \
	--port 8080 \
	--memory 1Gi \
	--region <IMAGE_REGION> \
	--allow-unauthenticated \
	--image us-east1-docker.pkg.dev/<PROJECT_ID>/<IMAGES_FOLDER>/<IMAGE_NAME>:latest \
	--add-cloudsql-instances <PROJECT_ID>:<CLOUDSQL_INSTANCE_REGION>:<CLOUDSQL_INSTANCE_NAME> \
	--set-env-vars USER=<DB_USER>,PASSWORD=<DB_PASSWORK>,CLOUD_SQL_IP_ADDRESS=<CLOUDSQL_PUBLIC_IP_ADDRESS>,DB_NAME=<DB_NAME>,CLOUD_SQL_CONNECTION_NAME=<PROJECT_ID>:<CLOUDSQL_INSTANCE_REGION>:<CLOUDSQL_INSTANCE_NAME>,DATABASE_URL=mysql+pymysql://${USER}:${PASSWORD}@/${DB_NAME}?unix_socket=/cloudsql/${CLOUD_SQL_CONNECTION_NAME}
