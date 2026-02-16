#!/bin/bash

echo "=== Mini Me Deploy ==="

cd ~/mini_me

# Pull latest code
git pull origin main || { echo "ERROR: git pull failed"; exit 1; }

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
$DC build || { echo "ERROR: build failed"; exit 1; }
$DC up -d --force-recreate || { echo "ERROR: up failed"; exit 1; }

# Wait for ingestion + server startup, retry health check every 5s up to 90s
echo "Waiting for server to start..."
HEALTHY=false
for i in $(seq 1 18); do
    echo "  Health check attempt $i/18..."
    if curl -sf http://localhost:8000/api/health 2>&1; then
        echo ""
        echo "=== Health check passed ==="
        HEALTHY=true
        break
    fi
    sleep 5
done

if [ "$HEALTHY" = false ]; then
    echo "=== WARNING: Health check failed after 90s ==="
    $DC logs --tail 30
    exit 1
fi

# Clean up old images
docker image prune -f

echo "=== Deploy complete ==="
