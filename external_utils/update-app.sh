#!/bin/bash
set -e

echo "🚀 Updating Echoes Backend..."

# Navigate to project
cd ~/projects/echoes-backend

# Pull latest code
echo "📥 Pulling latest code..."
git pull

# Show latest commit
echo "📋 Latest commit:"
git log --oneline -1

# Build new image
echo "🔨 Building Docker image..."
docker build -t echoes-backend:latest .

# Update service
echo "🔄 Updating service..."
docker service update --image echoes-backend:latest echoes_api

# Wait a moment for update to start
sleep 5

# Check status
echo "✅ Update status:"
docker service ps echoes_api --filter "desired-state=running" --format "table {{.Name}}\t{{.CurrentState}}"

# Show logs
echo "📄 Recent logs:"
docker service logs echoes_api --tail 20

echo "✨ Update complete!"