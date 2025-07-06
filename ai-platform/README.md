# AI-as-a-Service Microservices Platform

This project is an AI-as-a-Service (AIaaS) platform built with a microservices architecture.

## Project Structure

- `gateway/`: The API Gateway that routes requests to the appropriate microservices.
- `services/`: Contains the individual AI microservices.
  - `text-gen/`: A service for text generation.
  - `sentiment-analyzer/`: A service for sentiment analysis.
  - `embeddings-service/`: A service for generating text embeddings.
- `shared/`: Contains shared libraries and utilities.
  - `logger/`: Shared logging functionality.
  - `auth/`: Shared authentication and authorization functionality.
- `docker-compose.yml`: Defines the services, networks, and volumes for the Dockerized application.

## Getting Started

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Laaliji/AIaaS_microservices_platform.git
    cd ai-platform
    ```

2.  **Build and run the services:**
    ```bash
    docker compose build
    docker compose up
    ```

3.  **Test the endpoints:**
    -   Gateway Healthcheck: [http://localhost:8000/health](http://localhost:8000/health)
    -   Text Generation: `http://localhost:8000/generate?text=Hello`
