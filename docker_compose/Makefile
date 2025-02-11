DC = docker -compose
STORAGES_FILE = docker_compose/app.yaml
EXEC = docker exec -it
DB_CONTAINER = mongoDB
LOGS = docker logs
ENV_FILE = --env-file .env

.PHONY: storages
storages:
	$(DC) -f $(STORAGES_FILE) $(ENV_FILE) up -d

.PHONY: storages-down
storages-down:
	$(DC) -f $(STORAGES_FILE) down

.PHONY: storages-logs
storages-logs:
	$(LOGS) -f $(DB_CONTAINER) -f