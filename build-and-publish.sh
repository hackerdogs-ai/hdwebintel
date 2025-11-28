#!/bin/bash

# Script to build and publish Docker images

set -e

# Configuration
IMAGE_NAME="tredkar/webintel"
VERSION_TAG="3.0"
LATEST_TAG="latest"
BUILD_MEMORY="6g"

echo "=========================================="
echo "Building Docker Images"
echo "=========================================="

# Build the API image
echo "Building API image..."
sudo DOCKER_BUILDKIT=1 docker build \
    -m "$BUILD_MEMORY" \
    -t "${IMAGE_NAME}-api:${VERSION_TAG}" \
    -t "${IMAGE_NAME}-api:${LATEST_TAG}" \
    -f Dockerfile.api \
    .

# Build the MCP image
echo "Building MCP image..."
sudo DOCKER_BUILDKIT=1 docker build \
    -m "$BUILD_MEMORY" \
    -t "${IMAGE_NAME}-mcp:${VERSION_TAG}" \
    -t "${IMAGE_NAME}-mcp:${LATEST_TAG}" \
    -f Dockerfile.mcp \
    .

echo ""
echo "=========================================="
echo "Publishing Docker Images"
echo "=========================================="

# Check if user is logged in to Docker Hub
if ! sudo docker info 2>/dev/null | grep -q "Username"; then
    echo "Please login to Docker Hub first:"
    echo "  sudo docker login -u tredkar"
    read -p "Press Enter after logging in, or Ctrl+C to skip publishing..."
fi

# Push API image
echo "Pushing API image..."
sudo docker push "${IMAGE_NAME}-api:${VERSION_TAG}"
sudo docker push "${IMAGE_NAME}-api:${LATEST_TAG}"

# Push MCP image
echo "Pushing MCP image..."
sudo docker push "${IMAGE_NAME}-mcp:${VERSION_TAG}"
sudo docker push "${IMAGE_NAME}-mcp:${LATEST_TAG}"

echo ""
echo "=========================================="
echo "Build and Publish Complete!"
echo "=========================================="
echo "Images published:"
echo "  - ${IMAGE_NAME}-api:${VERSION_TAG}"
echo "  - ${IMAGE_NAME}-api:${LATEST_TAG}"
echo "  - ${IMAGE_NAME}-mcp:${VERSION_TAG}"
echo "  - ${IMAGE_NAME}-mcp:${LATEST_TAG}"

