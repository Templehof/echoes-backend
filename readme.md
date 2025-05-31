# Echoes Backend - Production Deployment Guide

This guide explains how to deploy the Echoes Backend to production using Docker Swarm for secure secret management.

## Prerequisites

- Ubuntu/Debian server with Docker installed
- Docker Swarm initialized (`docker swarm init`)
- Git access to pull this repository

## Initial Setup

### 1. Clone the Repository

```bash
cd ~
git clone [your-repo-url] echoes-backend
cd echoes-backend
# Navigate to production directory
cd production

# Copy the example file
cp .env.production.example .env.production

# Edit with your actual production values
nano .env.production

GOOGLE_MAPS_API_KEY=your-actual-google-maps-api-key
APP_NAME=Echoes Backend Production
ENVIRONMENT=production
DEBUG=false

# Make the script executable
chmod +x create-secrets.sh

# Create the secrets
./create-secrets.sh

# Go back to project root
cd ~/echoes-backend

# Build the image
docker build -t echoes-backend:latest .

# Deploy using Docker Swarm
docker stack deploy -c docker-stack.yml echoes

## Common operations

# Update Application Code
cd ~/echoes-backend

# Pull latest changes
git pull

# Rebuild the image
docker build -t echoes-backend:latest .

# Update the running service
docker service update --image echoes-backend:latest echoes_api

# Update Secrets
If you need to change environment variables:

cd ~/echoes-backend/production

# Edit the environment file
nano .env.production

# Recreate secrets
./create-secrets.sh

# Force service restart to pick up new secrets
docker service update --force echoes_api

# View Logs
bash# Stream logs
docker service logs echoes_api -f

# View last 100 lines
docker service logs echoes_api --tail 100

# Scale the Service
Scale to 3 replicas
docker service scale echoes_api=3

# Scale back to 1
docker service scale echoes_api=1
Remove the Stack
Remove entire stack
docker stack rm echoes

# Verify removal
docker service ls