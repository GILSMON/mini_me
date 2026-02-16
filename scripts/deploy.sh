#!/bin/bash
set -e

echo "=== Mini Me Deploy ==="

cd ~/mini_me

# Pull latest code
git pull origin main

# Detect docker compose command (v2 vs v1)
if docker compose version &> /dev/null; then
    DC="docker compose"
elif docker-compose version &> /dev/null; then
    DC="docker-compose"
else
    echo "ERROR: Neither 'docker compose' nor 'docker-compose' found"
    exit 1
fi

echo "Using: $DC"

# Build and restart containers
$DC build
$DC up -d --force-recreate

# Wait and check health
sleep 5
if curl -sf http://localhost:8000/api/health > /dev/null; then
    echo "=== Health check passed ==="
else
    echo "=== WARNING: Health check failed ==="
    $DC logs --tail 20
    exit 1
fi

# Clean up old images
docker image prune -f

echo "=== Deploy complete ==="
