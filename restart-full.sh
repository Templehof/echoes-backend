#!/bin/bash
set -e

echo "🚀 Full Restart of Echoes Backend..."
echo "=================================="

# Navigate to project
cd ~/projects/echoes-backend

# Stop everything first
echo "🛑 Stopping all services..."
docker stack rm echoes 2>/dev/null || echo "No stack to remove"

# Wait for services to fully stop
echo "⏳ Waiting for services to stop..."
count=0
while [ $(docker ps --filter "name=echoes" -q | wc -l) -gt 0 ] && [ $count -lt 30 ]; do
    sleep 1
    count=$((count + 1))
    echo -n "."
done
echo ""

# Verify stopped
if [ $(docker ps --filter "name=echoes" -q | wc -l) -gt 0 ]; then
    echo "⚠️  Warning: Some containers still running"
    docker ps --filter "name=echoes"
else
    echo "✅ All services stopped"
fi

# Pull latest code
echo ""
echo "📥 Pulling latest code..."
git pull

# Show latest commit
echo "📋 Latest commit:"
git log --oneline -1

# Build new image
echo ""
echo "🔨 Building Docker image..."
docker build -t echoes-backend:latest .

# Recreate secrets if needed
echo ""
echo "🔑 Checking secrets..."
if [ -f "production/.env.production" ]; then
    echo "Refreshing secrets from production/.env.production..."
    cd production
    ./create-secrets.sh
    cd ..
else
    echo "Using existing secrets"
    docker secret ls
fi

# Deploy the stack
echo ""
echo "📦 Deploying stack..."
docker stack deploy -c docker-stack.yml echoes

# Wait for services to start
echo ""
echo "⏳ Waiting for services to start..."
count=0
while [ $(docker service ls --filter "name=echoes_api" --format "{{.Replicas}}" | grep -o "1/1" | wc -l) -eq 0 ] && [ $count -lt 60 ]; do
    sleep 2
    count=$((count + 2))
    echo -n "."
done
echo ""

# Check final status
echo ""
echo "📊 Service status:"
docker service ls --filter "name=echoes"
echo ""
docker service ps echoes_api --no-trunc --format "table {{.Name}}\t{{.CurrentState}}\t{{.Error}}"

# Show logs
echo ""
echo "📄 Recent logs:"
docker service logs echoes_api --tail 30

# Health check
echo ""
echo "🏥 Health check:"
sleep 3
if curl -f -s http://localhost/health > /dev/null 2>&1; then
    echo "✅ API is responding"
    curl -s http://localhost/health | python3 -m json.tool 2>/dev/null || curl http://localhost/health
else
    echo "❌ API is not responding yet"
    echo "   Run 'docker service logs echoes_api -f' to see what's happening"
fi

echo ""
echo "✨ Full restart complete!"
echo ""
echo "Useful commands:"
echo "  - Check logs:    docker service logs echoes_api -f"
echo "  - Check status:  docker service ps echoes_api"
echo "  - Check health:  curl http://localhost/health"