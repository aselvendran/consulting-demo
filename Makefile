shell := bin/bash


.PHONY: launch-minikube
launch-minikube:
	minikube start --mount-string $(shell realpath .):/consulting-demo --mount --driver=docker

.PHONY: install-localstack-helmchart
install-localstack-helmchart:
	helm repo add localstack-repo https://helm.localstack.cloud
	helm upgrade --install localstack localstack-repo/localstack

.PHONY: expose-port-for-localstack
expose-port-for-localstack:
	kubectl port-forward $(shell kubectl get pod -l app.kubernetes.io/name=localstack --no-headers -o custom-columns=":metadata.name") 4566:4566


.PHONY: run-postgres-container
run-postgres-container:
	docker build . -t consulting-demo
	docker run -d --name consulting-demo-container -p 5432:5432 consulting-demo

.PHONY: run-lapsed-workflow-scenarios
run-lapsed-workflow-scenarios:
	docker build -f Dockerfile.dbt . -t demo_consulting
	docker run --env-file .env_sample  --network host --rm -it --entrypoint bash demo_consulting -c "python data_gathering/workflow_scenarios/lapsed_window/main.py"

.PHONY: run-dbt-models
run-dbt-models:
	docker build -f Dockerfile.dbt . -t demo_consulting
	docker run --env-file .env_sample --network host --rm -it --entrypoint bash demo_consulting -c "cd analytics && dbt run"

.PHONY: stop-remove-docker-container
stop-remove-docker-container:
	docker stop consulting-demo-container
	docker rm consulting-demo-container


.PHONY: destroy-minikube
destroy-minikube:
	minikube stop
	minikube delete
