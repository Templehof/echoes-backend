#!/bin/bash

# Read .env.production and create Docker secrets
while IFS='=' read -r key value; do
    # Skip empty lines and comments
    [[ -z "$key" || "$key" =~ ^[[:space:]]*# ]] && continue

    # Remove quotes if present
    value="${value%\"}"
    value="${value#\"}"

    # Create secret (lowercase name)
    secret_name=$(echo "$key" | tr '[:upper:]' '[:lower:]')

    # Remove existing secret if it exists
    docker secret rm "$secret_name" 2>/dev/null || true

    # Create new secret
    echo "$value" | docker secret create "$secret_name" -
    echo "Created secret: $secret_name"
done < .env.production

echo "Done! Current secrets:"
docker secret ls