# CI/CD Pipeline for AI Platform

This directory contains the CI/CD configuration for the AI Platform project.

## Workflows

### `ci.yml`

This workflow runs on every push to the main/master branch and on pull requests. It:

1. **Tests** each service with pytest
2. **Builds** Docker images for each service

## Adding Tests

To add tests for a service:

1. Create a `tests` directory in the service's folder
2. Add test files with names starting with `test_`
3. Run tests locally with `pytest`

## Future Enhancements

Planned enhancements for the CI/CD pipeline:

1. **Deployment** to development/staging/production environments
2. **Security scanning** of Docker images
3. **Performance testing** for API endpoints
4. **Integration testing** between services
