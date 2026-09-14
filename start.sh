#!/bin/bash

# The Lenny Growth Assistant - Quick Start Script
# This script starts all services using Docker Compose

set -e

echo "================================"
echo "The Lenny Growth Assistant"
echo "Quick Start"
echo "================================"
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running"
    echo "Please start Docker and try again"
    exit 1
fi

echo "✓ Docker is running"
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found"
    echo "Creating .env from .env.example..."
    cp .env.example .env
    echo "✓ .env file created"
    echo ""
fi

echo "Starting services with Docker Compose..."
echo ""
echo "Services:"
echo "  - PostgreSQL  (port 5432)"
echo "  - Backend API (port 8000)"
echo "  - Frontend    (port 5173)"
echo ""

docker compose up --build
