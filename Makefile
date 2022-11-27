DEV_ENV_FILE=.env.dev
PROD_ENV_FILE=.env.prod

BASE_COMPOSE_FILE=docker-compose.yml
DEV_COMPOSE_FILE=docker-compose.dev.yml
PROD_COMPOSE_FILE=docker-compose.prod.yml

# Development commands

dev:
	@echo "Building the project in the development mode"
	make build ENV_FILE=$(DEV_ENV_FILE) COMPOSE_FILE=$(DEV_COMPOSE_FILE)
	@echo "Running the project as a daemon in the development mode"
	make run ENV_FILE=$(DEV_ENV_FILE) COMPOSE_FILE=$(DEV_COMPOSE_FILE)

dev-stop:
	make stop ENV_FILE=$(DEV_ENV_FILE) COMPOSE_FILE=$(DEV_COMPOSE_FILE)

# Production commands

prod:
	@echo "Building the project in the production mode"
	make build ENV_FILE=$(PROD_ENV_FILE) COMPOSE_FILE=$(PROD_COMPOSE_FILE)
	@echo "Running the project as a daemon in the production mode"
	make run ENV_FILE=$(PROD_ENV_FILE) COMPOSE_FILE=$(PROD_COMPOSE_FILE)

prod-stop:
	make stop ENV_FILE=$(PROD_ENV_FILE) COMPOSE_FILE=$(PROD_COMPOSE_FILE)

# Base

build:
	docker compose --env-file $(ENV_FILE) -f $(BASE_COMPOSE_FILE) -f $(COMPOSE_FILE) build

run:
	docker compose --env-file $(ENV_FILE) -f $(BASE_COMPOSE_FILE) -f $(COMPOSE_FILE) up -d

stop:
	docker compose --env-file $(ENV_FILE) -f $(BASE_COMPOSE_FILE) -f $(COMPOSE_FILE) down
