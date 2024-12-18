#!/bin/bash

# Variables
DOCKER_IMAGE="marloeni/snowradar"
CONTAINER_NAME="snowradar"
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
-e DB_NAME=snowradar \
-e DB_USER=marloeni \
-e DB_PASSWORD=1234 \
-e DB_HOST=127.0.0.1 \
-e DB_PORT=5432 \
"$DOCKER_IMAGE:latest"
EOF
