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
   ```
2. Install dependencies:
   ```bash
   make install
   ```
3. Source env:
   ```bash
   source .venv/bin/activate
   ```
4. Build Docker Image
   ```
   make build
   ```

## Run
### Local
`make app-run`
### Docker
`make run`

## Test
### Local
`make test-local`
### Docker
`make test`

## Utilities
`make shell`
`make rebuild`
`make clean`
`make docker-clean`