# Variables
IMAGE_NAME := social-media-insights
CONTAINER_NAME := social-media-insights-container
DATA_VOLUME := $(shell pwd)/data:/data
APP_VOLUME := $(shell pwd)/app:/app
DOCKER_RUN_FLAGS := --rm --name $(CONTAINER_NAME) -v $(DATA_VOLUME) -v $(APP_VOLUME)
PYTHON := python3

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
	docker build -t $(IMAGE_NAME) .

# Run the Docker container
.PHONY: run
run: ## Run the application in the Docker container
	@echo "Running the Docker container..."
	docker run $(DOCKER_RUN_FLAGS) $(IMAGE_NAME)

# Run the application in interactive mode
.PHONY: interactive
interactive: ## Run the container in interactive mode
	@echo "Starting the Docker container in interactive mode..."
	docker run -it $(DOCKER_RUN_FLAGS) $(IMAGE_NAME) bash

# Run tests
.PHONY: test
test: ## Run tests inside the Docker container
	@echo "Running tests..."
	docker run $(DOCKER_RUN_FLAGS) $(IMAGE_NAME) pytest

# Stop and remove containers
.PHONY: clean-containers
clean-containers: ## Stop and remove the Docker container
	@echo "Cleaning up containers..."
	-docker stop $(CONTAINER_NAME) 2>/dev/null || true
	-docker rm $(CONTAINER_NAME) 2>/dev/null || true

# Clean up environment
.PHONY: clean
clean: clean-containers ## Clean up temporary files and environment
	@rm -rf .venv
	@find . -name "__pycache__" -type d -exec rm -rf {} +
	@echo "Environment and cache cleaned up."

# Initialize the uv project
.PHONY: install
install: ## install requirements
	@uv pip install -r requirements.txt
	@uv sync

# Rebuild the project
.PHONY: rebuild
rebuild: clean install ## Clean and reinstall the project
	@echo "Rebuilt the project."

# Run the application
.PHONY: app-run
app-run: ## Run the application using uv
	@uv run python -m app.etl