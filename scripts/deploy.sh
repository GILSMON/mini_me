#!/bin/bash
set -e

echo "=== Mini Me Deploy ==="

cd ~/mini_me

# Pull latest code
git pull origin main

# Build and restart containers
docker compose build --no-cache
docker compose up -d --force-recreate

# Wait and check health
sleep 5
if curl -sf http://localhost:8000/api/health > /dev/null; then
    echo "=== Health check passed ==="
else
    echo "=== WARNING: Health check failed ==="
    docker compose logs --tail 20
    exit 1
fi

# Clean up old images
docker image prune -f

echo "=== Deploy complete ==="
