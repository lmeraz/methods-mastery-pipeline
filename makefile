# Variables
COMPOSE := docker-compose
SERVICE := etl
UV := uv

# Default target
.DEFAULT_GOAL := help

# Help target
.PHONY: help
help: ## Display this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

# Build the Docker image
.PHONY: build
build: ## Build the Docker image
	@echo "Building the Docker image..."
	$(COMPOSE) build

# Start the application
.PHONY: up
up: ## Start the application
	@echo "Starting the application..."
	$(COMPOSE) up

# Stop the application
.PHONY: down
down: ## Stop the application and remove containers
	@echo "Stopping the application..."
	$(COMPOSE) down

# Rebuild the application
.PHONY: rebuild
rebuild: ## Rebuild and restart the application
	@echo "Rebuilding the application..."
	$(COMPOSE) down
	$(COMPOSE) build
	$(COMPOSE) up

# Run tests
.PHONY: test
test: build ## Build the image and run tests
	@echo "Running tests..."
	$(COMPOSE) run --rm $(SERVICE) pytest

# Open an interactive shell in the container
.PHONY: shell
shell: ## Open an interactive shell in the container
	@echo "Opening interactive shell..."
	$(COMPOSE) exec $(SERVICE) /bin/sh

# Clean up the environment
.PHONY: clean
clean: down ## Clean up environment and temporary files
	@echo "Cleaning up environment..."
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "Environment cleaned up."

# Remove unused Docker resources
.PHONY: docker-clean
docker-clean: ## Remove unused Docker containers, images, and volumes
	@echo "Cleaning up Docker resources..."
	docker container prune -f
	docker image prune -f
	docker volume prune -f
	docker network prune -f
	@echo "Docker cleanup complete."

# Initialize the UV project locally
.PHONY: install
install: ## Install requirements for the local UV project
	@echo "Installing dependencies for the UV project..."
	uv pip install -r requirements.txt
	uv sync
	uv run pre-commit install

# Run the application locally
.PHONY: app-run
app-run: ## Run the application using the UV project
	@echo "Running the application locally with UV..."
	PYTHONPATH=$(shell pwd) $(UV) run app/etl.py

# Run tests locally with UV
.PHONY: test-local
test-local: ## Run tests locally using the UV project
	@echo "Running tests locally with UV..."
	PYTHONPATH=$(shell pwd) $(UV) pytest