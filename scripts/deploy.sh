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

# Wait for ingestion + server startup, retry health check every 5s up to 60s
echo "Waiting for server to start..."
for i in $(seq 1 12); do
    if curl -sf http://localhost:8000/api/health > /dev/null 2>&1; then
        echo "=== Health check passed ==="
        break
    fi
    if [ "$i" -eq 12 ]; then
        echo "=== WARNING: Health check failed after 60s ==="
        $DC logs --tail 30
        exit 1
    fi
    sleep 5
done

# Clean up old images
docker image prune -f

echo "=== Deploy complete ==="
