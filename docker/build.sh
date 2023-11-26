#!/usr/bin/env bash

# Export dependencies from poetry
poetry export -f requirements.txt --output docker/requirements.txt --without-hashes

# Build docker image
docker  build -t langchain-docs-chatbot -f ./docker/Dockerfile .

# Run docker image and add data/ directory as volume
docker run --rm -p 8501:8501 -v ./data:/data --env-file .env langchain-docs-chatbot &&

# Remove dependencies
rm ./docker/requirements.txt
