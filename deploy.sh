#!/bin/bash

# Variables
DOCKER_IMAGE="marloeni/snowradar-etl"
CONTAINER_NAME="snowradar-etl"
SSH_HOST="69.48.205.81"
SSH_USER="root"
SSH_KEY="~/.ssh/id_ed25519"

# Build and push Docker image
docker buildx build --platform linux/amd64,linux/arm64 -t "$DOCKER_IMAGE:latest" --push . || exit 1

# Deploy to server
ssh -i $SSH_KEY $SSH_USER@$SSH_HOST <<EOF

# Pull the latest Docker image
docker image pull "$DOCKER_IMAGE:latest"

# Stop and remove any existing container with the same name
docker stop "$CONTAINER_NAME" || true
docker rm "$CONTAINER_NAME" || true

# Run the new container with host network
docker run -d --name "$CONTAINER_NAME" \
--network host \
"$DOCKER_IMAGE:latest"
EOF
