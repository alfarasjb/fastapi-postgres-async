# Define the default target
.DEFAULT_GOAL := up

# Load environment variables from .env file
ifneq (,$(wildcard .env))
    include .env
    export
endif

# Set COMPOSE_FILES to always use docker-compose.yml
COMPOSE_FILES = -f docker-compose.yml

# Target to start the services
up:
	@echo "Starting services with Docker Compose..."
	docker-compose $(COMPOSE_FILES) up -d

# Target to stop the services and remove related containers and images
down:
	@echo "Stopping services with Docker Compose..."
	docker-compose $(COMPOSE_FILES) down
	@echo "Removing stopped containers..."
	docker-compose $(COMPOSE_FILES) rm -f
	@echo "Removing related images..."
	docker rmi -f custom-pgvector


# Target to build the services
build:
	@echo "Building services with Docker Compose..."
	docker-compose $(COMPOSE_FILES) build

# Target to view logs
logs:
	@echo "Viewing logs for services..."
	docker-compose $(COMPOSE_FILES) logs -f

# Target to print the value of ENABLE_FASTAPI
print-env:
	@echo "DATABASE_URL: $(DATABASE_URL)"


migrate:
	@echo "Running alembic migrations with Docker Compose..."
	docker-compose -f docker-compose.fastapi.yml run fastapi alembic upgrade head