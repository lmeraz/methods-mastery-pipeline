# Social Media Insights Tracker

## Overview
This project extracts, transforms, and loads social media post data into a SQLite database using the Hugging Face `datasets` library. It generates insights about the data and is containerized with Docker.

## Features
- ETL pipeline to handle large datasets.
- Insights generation and upsertion into SQLite.
- Dependency management with `astral-sh/uv`.
- Containerized with Docker for deployment.

## Requirements
- Python 3.10+
- Docker
- Astral-sh/UV

## Usage

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd social-media-insights
2. Install dependencies:
   make install
3. Run the ETL pipeline:
   make app-run
4. run the application in Docker:
   make build
5. Run on docker container
   make run
6. Run tests o docker container
   make tests