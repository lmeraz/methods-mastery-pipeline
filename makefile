# Variables
COMPOSE := docker-compose
SERVICE := etl
CONTAINER_NAME := social-media-insights-container
IMAGE_NAME := social-media-insights
DATA_VOLUME := $(shell pwd)/data:/data

# Default target
.DEFAULT_GOAL := help

# Help target
.PHONY: help
help: ## Display this help message
	@echo "Available targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'

# Build the Docker image
build: ## Build the Docker image using Docker Compose
	@echo "Building the Docker image..."
	$(COMPOSE) build

# Start the application
.PHONY: up
up: ## Start the application using Docker Compose
	@echo "Starting the application..."
	$(COMPOSE) up

# Stop the application
.PHONY: down
down: ## Stop the application and remove containers
	@echo "Stopping the application..."
	$(COMPOSE) down

# Run tests
.PHONY: test
test: ## Run tests inside the Docker Compose service
	@echo "Running tests..."
	$(COMPOSE) run $(SERVICE) pytest

# Clean up environment
.PHONY: clean
clean: down ## Clean up temporary files and environment
	@echo "Cleaning up environment..."
	@rm -rf .venv
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "Environment and cache cleaned up."

# Initialize the uv project
.PHONY: install
install: ## install requirements
	@uv pip install -r requirements.txt
	@uv sync


.PHONY: rebuild
rebuild: ## Rebuild the application
	@echo "Rebuilding the application..."
	$(COMPOSE) down
	$(COMPOSE) build
	$(COMPOSE) up

# Run the application
.PHONY: app-run
app-run: ## Run the application using uv
	@uv run app/etl.py

# Run interactive shell
.PHONY: shell
shell: ## Open an interactive shell inside the container
	@echo "Opening interactive shell..."
	$(COMPOSE) exec $(SERVICE) /bin/sh