#!/bin/bash

# Usage: ./run_docker.sh [envfile]
# Default: .env

ENVFILE=${1:-.env}

# Build the Docker image
docker build -t farfetchr-backend .

# Stop and remove any existing container with the same name
docker stop farfetchr-backend-container 2>/dev/null || true
docker rm farfetchr-backend-container 2>/dev/null || true

# Check if port 8000 is in use by any container and stop/remove it
CONTAINER_ID=$(docker ps -q --filter "publish=8000")
if [ -n "$CONTAINER_ID" ]; then
  echo "Port 8000 is in use by container $CONTAINER_ID. Stopping and removing it..."
  docker stop $CONTAINER_ID
  docker rm $CONTAINER_ID
fi

# Check if port 8000 is in use by any process (not just Docker)
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null ; then
  echo "Port 8000 is still in use by a non-Docker process. Please free the port and try again."
  exit 1
fi

# Run the Docker container
docker run --env-file $ENVFILE -p 8000:8000 --name farfetchr-backend-container farfetchr-backend 