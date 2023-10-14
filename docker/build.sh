#!/usr/bin/env bash

# Export dependencies from poetry
poetry export -f requirements.txt --output docker/requirements.txt --without-hashes

# Build docker image
docker build -t langchain-docs-chatbot ./docker

# Run docker image
docker run --rm -p 5005:5005 langchain-docs-chatbot

# Remove dependencies
rm ./requirements.txt

