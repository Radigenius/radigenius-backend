# RadiGenius - AI-Powered Chat Interface

<p align="center">
<a href="https://www.python.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/python/python-original.svg" alt="python" width="40" height="40"/> </a>
<a href="https://www.djangoproject.com/" target="_blank"> <img src="https://user-images.githubusercontent.com/29748439/177030588-a1916efd-384b-439a-9b30-24dd24dd48b6.png" alt="django" width="60" height="40"/> </a> 
<a href="https://fastapi.tiangolo.com/" target="_blank"> <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" alt="fastapi" height="40"/> </a>
<a href="https://www.docker.com/" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/docker/docker-original-wordmark.svg" alt="docker" width="40" height="40"/> </a>
<a href="https://www.postgresql.org" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/postgresql/postgresql-original-wordmark.svg" alt="postgresql" width="40" height="40"/> </a>
<a href="https://www.nginx.com" target="_blank"> <img src="https://raw.githubusercontent.com/devicons/devicon/master/icons/nginx/nginx-original.svg" alt="nginx" width="40" height="40"/> </a>
</p>

[![Code Style Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

## Project Overview

RadiGenius is a chat interface application that connects users to an AI model through a Django backend and a FastAPI inference service. The system is designed with clean architecture principles to ensure maintainability, scalability, and separation of concerns.

## Table of Contents

- [Project Structure](#project-structure)
- [Environment Configuration](#environment-configuration)
- [Setup and Installation](#setup-and-installation)
  - [Development Setup](#development-setup)
  - [Production Setup](#production-setup)
- [API Documentation](#api-documentation)
- [Security](#security)
- [Contributing](#contributing)
- [License](#license)

## Project Structure

The project consists of two main components:

### 1. RadiGenius Backend (Django)
- Django-based REST API with DRF
- Handles user authentication, conversation management, and business logic
- Communicates with the Inference API for AI model responses
- Follows clean architecture principles with layers:
  - Domain (entities, use cases)
  - Infrastructure (settings, database)
  - Interface adapters (controllers, presenters)
  - Frameworks & drivers (web, UI)

### 2. RadiGenius Inference API (FastAPI)
- FastAPI service for AI model inference
- Handles chat completions and other inference-related operations
- Optimized for performance with async operations
- Exposed endpoints for the backend to consume

## Environment Configuration

The project uses environment variables for configuration. Key variables include:

### Backend Environment (.env)

```
# General
SECRET_KEY=           # Django secret key
DEBUG=False           # Enable/disable debug mode
ALLOWED_HOSTS=        # Comma-separated list of allowed hosts
APP_NAME=radigenius   # Application name
CDN_URL=              # CDN URL for static files
INFERENCE_SERVICE_URL= # URL to the FastAPI inference service

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=              # Database name
DB_USER=              # Database user
DB_PASS=              # Database password
DB_HOST=              # Database host
DB_PORT=              # Database port

# Logs and monitoring
SEQ_LOG_LEVEL=INFO
SENTRY_DSN=           # Sentry DSN for error tracking

# Email
EMAIL_HOST=           # SMTP host
EMAIL_PORT=           # SMTP port
```

See the complete list of environment variables in the `.env.sample` files in the repository.

## Setup and Installation

### Prerequisites

- Docker and Docker Compose
- Git

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/your-username/radigenius.git
cd radigenius
```

2. Copy sample env files:
```bash
cp radigenius-backend/envs/dev/backend/.env.sample radigenius-backend/envs/dev/backend/.env
cp radigenius-inference-api/envs/dev/.env.sample radigenius-inference-api/envs/dev/.env
```

3. Update environment variables in the .env files

4. Build and run the development environment:
```bash
docker-compose -f docker/docker-compose.yml up --build
```

5. Access the application at http://localhost:8000

### Production Setup

1. Set up production environment:
```bash
cp radigenius-backend/envs/prod/backend/.env.sample radigenius-backend/envs/prod/backend/.env
cp radigenius-inference-api/envs/prod/.env.sample radigenius-inference-api/envs/prod/.env
```

2. Update environment variables with production values

3. Build and run with production settings:
```bash
docker-compose -f docker-compose-prod.yml up --build
```

## API Documentation

- Backend API documentation is available at `/api/docs/` once the server is running
- Inference API documentation is available at `/docs` on the inference service

## Security

The project implements several security best practices:
- JWT authentication
- HTTPS enforcement in production
- Admin panel protection with rate limiting and honeypot
- Proper CORS configuration
- Security headers implementation

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT
