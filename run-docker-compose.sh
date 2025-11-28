#!/bin/bash

# Script to run docker-compose

set -e

# Check if certificates exist
if [ ! -d "./certs" ] || [ ! -f "./certs/web-cert.pem" ] || [ ! -f "./certs/mcp-cert.pem" ]; then
    echo "Certificates not found. Generating certificates..."
    if [ -f "./generate-certificates.sh" ]; then
        chmod +x ./generate-certificates.sh
        ./generate-certificates.sh
    else
        echo "Error: generate-certificates.sh not found!"
        echo "Please run generate-certificates.sh first to create SSL certificates."
        exit 1
    fi
fi

echo "=========================================="
echo "Starting Docker Compose Services"
echo "=========================================="

# Check if docker-compose is available
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif command -v docker &> /dev/null && docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "Error: docker-compose or docker compose not found!"
    exit 1
fi

# Parse command line arguments
ACTION="${1:-up}"
OPTIONS="${2:--d}"

case "$ACTION" in
    up)
        echo "Starting services in detached mode..."
        $COMPOSE_CMD up -d
        ;;
    down)
        echo "Stopping services..."
        $COMPOSE_CMD down
        ;;
    restart)
        echo "Restarting services..."
        $COMPOSE_CMD restart
        ;;
    logs)
        echo "Showing logs..."
        $COMPOSE_CMD logs -f
        ;;
    ps)
        echo "Service status:"
        $COMPOSE_CMD ps
        ;;
    build)
        echo "Building services..."
        $COMPOSE_CMD build
        ;;
    *)
        echo "Usage: $0 {up|down|restart|logs|ps|build} [options]"
        echo ""
        echo "Examples:"
        echo "  $0 up          # Start services in detached mode"
        echo "  $0 up --build  # Build and start services"
        echo "  $0 down        # Stop services"
        echo "  $0 restart     # Restart services"
        echo "  $0 logs        # Show logs"
        echo "  $0 ps          # Show service status"
        exit 1
        ;;
esac

if [ "$ACTION" = "up" ]; then
    echo ""
    echo "=========================================="
    echo "Services Started!"
    echo "=========================================="
    echo "API Service:"
    echo "  HTTP:  http://localhost:5000"
    echo "  HTTPS: https://localhost:5443"
    echo ""
    echo "MCP Service:"
    echo "  HTTP:  http://localhost:8004"
    echo "  HTTPS: https://localhost:8443"
    echo ""
    echo "Note: Self-signed certificates are used. You may need to accept the certificate warning in your browser."
    echo ""
    echo "To view logs: $0 logs"
    echo "To stop services: $0 down"
fi

