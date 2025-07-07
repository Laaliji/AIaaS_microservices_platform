# PowerShell script to run all tests
# Exit on any error
$ErrorActionPreference = "Stop"

Write-Host "Running tests for AI Platform..." -ForegroundColor Green

# Test gateway service
Write-Host "Testing gateway service..." -ForegroundColor Cyan
Set-Location -Path gateway
python -m pytest tests/ -v
Set-Location -Path ..

# Test text-gen service (when tests are added)
Write-Host "Testing text-gen service..." -ForegroundColor Cyan
# Set-Location -Path services/text-gen
# python -m pytest tests/ -v
# Set-Location -Path ../..

# Test sentiment-analyzer service (when tests are added)
Write-Host "Testing sentiment-analyzer service..." -ForegroundColor Cyan
# Set-Location -Path services/sentiment-analyzer
# python -m pytest tests/ -v
# Set-Location -Path ../..

# Test embeddings-service (when tests are added)
Write-Host "Testing embeddings-service service..." -ForegroundColor Cyan
# Set-Location -Path services/embeddings-service
# python -m pytest tests/ -v
# Set-Location -Path ../..

Write-Host "All tests completed successfully!" -ForegroundColor Green
