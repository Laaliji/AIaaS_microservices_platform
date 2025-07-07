#!/bin/bash

# Exit on any error
set -e

echo "Running tests for AI Platform..."

# Test gateway service
echo "Testing gateway service..."
cd gateway
python -m pytest tests/ -v
cd ..

# Test text-gen service (when tests are added)
echo "Testing text-gen service..."
# cd services/text-gen
# python -m pytest tests/ -v
# cd ../..

# Test sentiment-analyzer service (when tests are added)
echo "Testing sentiment-analyzer service..."
# cd services/sentiment-analyzer
# python -m pytest tests/ -v
# cd ../..

# Test embeddings-service (when tests are added)
echo "Testing embeddings-service service..."
# cd services/embeddings-service
# python -m pytest tests/ -v
# cd ../..

echo "All tests completed successfully!"
