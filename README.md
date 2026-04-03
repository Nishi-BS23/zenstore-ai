# Zenstore AI

**Zenstore AI** is an enterprise-grade, production-ready FastAPI backend system designed for modern e-commerce and product management platforms. It delivers a comprehensive solution for authenticated product management, intelligent AI-powered content enrichment, scalable bulk data ingestion, and high-performance Redis-backed caching.

Built with a focus on **scalability**, **security**, and **maintainability**, the system implements a clean, layered architecture that separates concerns and ensures operational excellence in production environments.

## 🚀 Core Features

### Authentication & Security
- **JWT-based authentication** with bcrypt password hashing for secure user management
- **Role-based access control** with owner-scoped product operations
- **Secure session management** with configurable token expiration

### Product Management
- **RESTful CRUD APIs** for comprehensive product lifecycle management
- **Owner-scoped data isolation** ensuring multi-tenant security
- **Real-time validation** and robust error handling

### AI-Powered Enrichment
- **Asynchronous AI content generation** via Celery task queue
- **Multiple AI provider support** (Groq, OpenAI) with flexible configuration
- **Intelligent product descriptions** and metadata enhancement

### Data Processing & Storage
- **High-performance CSV bulk ingestion** with streaming row processing
- **Cache-aside Redis strategy** for optimal read performance
- **Repository pattern implementation** for consistent data access

### Testing & Quality Assurance
- **Comprehensive pytest suite** with isolated SQLite test database
- **Automated test fixtures** and deterministic test results
- **API contract testing** with full coverage validation

## 🛠️ Technology Stack

### Core Framework
- **FastAPI** - Modern, fast web framework for building APIs
- **SQLAlchemy** - Powerful ORM with advanced database operations
- **Alembic** - Database migration management system

### Background Processing & Caching
- **Celery** - Distributed task queue for async operations
- **Redis** - High-performance caching and message broker

### Security & Authentication
- **PyJWT** - JSON Web Token implementation
- **bcrypt** - Secure password hashing
- **python-multipart** - File upload handling

### Testing & Development
- **Pytest** - Feature-rich testing framework
- **TestClient** - FastAPI testing utilities
- **SQLite** - Lightweight database for testing

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Redis server
- AI provider account (Groq or OpenAI)

### Installation & Setup

1. **Clone and Setup Environment**
```bash
git clone <repository-url>
cd zenstore-ai
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. **Database Initialization**
```bash
# Apply database migrations
alembic upgrade head
```

4. **Start Services**
```bash
# Start Redis (if not already running)
redis-server

# Start the API server
uvicorn app.main:app --host 0.0.0.0 --port 9072 --reload

# Start Celery worker (in separate terminal)
celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

5. **Verify Installation**
```bash
# Health check
curl http://127.0.0.1:9072/health

# Explore API documentation
open http://127.0.0.1:9072/docs
```

## ⚙️ Configuration

The application reads configuration from environment variables, typically stored in a `.env` file in the project root.

### Environment Variables

```env
# Database Configuration
DATABASE_URL=sqlite:///./zenstore.db

# Security
SECRET_KEY=replace-with-a-long-random-secret-key-min-32-chars

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# AI Provider Configuration
AI_PROVIDER=groq
AI_MODEL=llama-3.1-8b-instant
GROQ_API_KEY=your-groq-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1

# Optional: Advanced Settings
# CELERY_BROKER_URL=redis://localhost:6379/1
# CACHE_TTL=3600
# MAX_UPLOAD_SIZE=10485760  # 10MB
```

### Configuration Reference

| Variable | Required | Purpose | Default Value | Example |
| --- | --- | --- | --- | --- |
| `DATABASE_URL` | ✅ | Database connection string | `sqlite:///./zenstore.db` | `postgresql://user:pass@host:5432/db` |
| `SECRET_KEY` | ✅ | JWT signing secret (min 32 chars) | None | `your-super-secret-key-32-chars-long` |
| `REDIS_URL` | ✅ | Redis URL for cache and Celery broker | `redis://localhost:6379/0` | `redis://redis:6379/0` |
| `AI_PROVIDER` | ✅ | AI provider selector | `groq` | `groq`, `openai` |
| `AI_MODEL` | ✅ | AI model identifier | `llama-3.1-8b-instant` | `gpt-4`, `llama-3.1-70b-instant` |
| `GROQ_API_KEY` | ✅ (if using Groq) | Groq API key | None | `gsk_...` |
| `OPENAI_API_KEY` | ✅ (if using OpenAI) | OpenAI API key | None | `sk-...` |
| `OPENAI_BASE_URL` | ❌ | Custom OpenAI endpoint | `https://api.openai.com/v1` | Custom endpoint URL |

## 🏗️ Architecture

### System Design Overview

Zenstore AI implements a **clean, layered architecture** that promotes separation of concerns, testability, and maintainability.

```mermaid
graph TB
    Client[Client Application] --> API[API Layer]
    API --> Auth[Authentication Middleware]
    API --> Service[Service Layer]
    Service --> Repo[Repository Layer]
    Service --> Cache[Redis Cache]
    Service --> Queue[Task Queue]
    Repo --> Model[Model Layer]
    Model --> DB[(Database)]
    Queue --> Worker[Background Workers]
    Worker --> AI[AI Services]
```

### Architecture Flow

```text
Request → API Layer → Service Layer → Repository Layer → Database
                ↓              ↓               ↓
            Validation    Business Logic   Data Access
                ↓              ↓               ↓
            Response     Cache/Queue     ORM Models
```

### Layer Responsibilities

#### 🔌 API Layer (`app/api/`)
- **Request validation** using Pydantic schemas
- **HTTP response formatting** and status codes
- **Dependency injection** for services and authentication
- **Route definitions** and API documentation
- **Error handling** and exception mapping

#### ⚙️ Service Layer (`app/services/`)
- **Business logic orchestration** and workflow coordination
- **Cross-cutting concerns** (caching, logging, metrics)
- **Transaction management** and data consistency
- **Integration with external services** (AI providers)
- **Background task queuing** via Celery

#### 🗄️ Repository Layer (`app/repositories/`)
- **Data access abstraction** using SQLAlchemy ORM
- **Query optimization** and database interactions
- **Entity lifecycle management** (CRUD operations)
- **Database-agnostic interface** for testing
- **Connection pooling** and performance tuning

#### 📋 Model Layer (`app/models/`)
- **SQLAlchemy ORM models** and database schema
- **Entity relationships** and constraints
- **Data validation** and type safety
- **Migration scripts** via Alembic
- **Indexing strategies** for performance

#### 🔄 Worker Layer (`app/workers/`)
- **Asynchronous task processing** with Celery
- **AI content generation** workflows
- **Bulk data processing** and enrichment
- **Error handling** and retry mechanisms
- **Task monitoring** and logging

### Design Benefits

- **Modularity**: Clear separation enables independent development and testing
- **Testability**: Each layer can be unit tested in isolation
- **Scalability**: Horizontal scaling possible at service and worker layers
- **Maintainability**: Well-defined boundaries reduce coupling and complexity
- **Flexibility**: Easy to swap components (databases, AI providers, caches)

## 🔄 Runtime Flows

### Authentication Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Auth
    participant DB

    Client->>API: POST /auth/register
    API->>Auth: Validate credentials
    Auth->>DB: Create user
    DB-->>Auth: User created
    Auth-->>API: Success
    API-->>Client: 201 Created

    Client->>API: POST /auth/login
    API->>Auth: Verify credentials
    Auth->>DB: Check user
    DB-->>Auth: User valid
    Auth-->>API: Generate JWT
    API-->>Client: 200 OK + JWT Token
```

### Product Creation Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant Repo
    participant DB
    participant Queue
    participant Worker

    Client->>API: POST /products + JWT
    API->>Service: create_product()
    Service->>Repo: insert_product()
    Repo->>DB: INSERT product
    DB-->>Repo: Product saved
    Repo-->>Service: Product ID
    Service->>Queue: enqueue_ai_task()
    Service-->>API: 202 Accepted
    API-->>Client: Product created

    Queue->>Worker: Process AI enrichment
    Worker->>Service: generate_ai_content()
    Service->>Repo: update_product()
    Repo->>DB: UPDATE with AI content
```

### Product Retrieval Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant Cache
    participant Repo
    participant DB

    Client->>API: GET /products/{id}
    API->>Service: get_product()
    Service->>Cache: Check cache
    alt Cache hit
        Cache-->>Service: Return cached data
    else Cache miss
        Service->>Repo: get_by_id()
        Repo->>DB: SELECT product
        DB-->>Repo: Product data
        Repo-->>Service: Product
        Service->>Cache: Store in cache
    end
    Service-->>API: Product data
    API-->>Client: 200 OK
```

### Bulk Upload Flow

```mermaid
sequenceDiagram
    participant Client
    participant API
    participant Service
    participant Queue
    participant Worker
    participant Repo
    participant DB

    Client->>API: POST /products/bulk + CSV
    API->>Service: process_bulk_upload()
    Service->>Service: Validate CSV
    Service->>Service: Stream rows
    loop Each row
        Service->>Repo: create_product()
        Repo->>DB: INSERT product
        DB-->>Repo: Product saved
        Service->>Queue: enqueue_ai_task(product_id)
    end
    Service-->>API: 202 Accepted + job_id
    API-->>Client: Upload started

    Queue->>Worker: Process AI tasks
    Worker->>Repo: update_products()
    Repo->>DB: UPDATE with AI content
```

## 📡 API Documentation

### Base URL
```
https://your-domain.com/api/v1
```

### Authentication
All protected endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <your-jwt-token>
```

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password123"
}
```
**Response:** `201 Created`

#### User Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "secure_password123"
}
```
**Response:** `200 OK`
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "token_type": "bearer"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer <token>
```
**Response:** `200 OK`

### Product Management Endpoints

#### Create Product
```http
POST /products
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Premium Widget",
  "description": "High-quality widget for professional use",
  "price": 99.99,
  "category": "electronics"
}
```
**Response:** `202 Accepted` (AI enrichment queued)

#### Get All Products
```http
GET /products
Authorization: Bearer <token>
Query Parameters:
- skip: int (default: 0)
- limit: int (default: 100)
```
**Response:** `200 OK`

#### Get Product by ID
```http
GET /products/{product_id}
Authorization: Bearer <token>
```
**Response:** `200 OK`

#### Update Product
```http
PUT /products/{product_id}
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Updated Widget Name",
  "price": 149.99
}
```
**Response:** `200 OK`

#### Delete Product
```http
DELETE /products/{product_id}
Authorization: Bearer <token>
```
**Response:** `204 No Content`

#### Bulk Upload Products
```http
POST /products/bulk
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: products.csv
```
**CSV Format:**
```csv
name,description,price,category
Product 1,Description 1,29.99,electronics
Product 2,Description 2,49.99,home
```
**Response:** `202 Accepted`
```json
{
  "message": "Bulk upload started",
  "job_id": "celery-task-uuid",
  "total_rows": 150
}
```

### Response Status Codes

| Status | Description | When Used |
|--------|-------------|-----------|
| `200 OK` | Success | Successful GET/PUT requests |
| `201 Created` | Resource Created | User registration |
| `202 Accepted` | Accepted | Async operations (product creation, bulk upload) |
| `204 No Content` | Success, No Content | DELETE operations |
| `400 Bad Request` | Invalid Input | Validation errors, invalid file format |
| `401 Unauthorized` | Authentication Required | Missing/invalid JWT token |
| `403 Forbidden` | Access Denied | User not owner of resource |
| `404 Not Found` | Resource Missing | Product/user not found |
| `422 Unprocessable Entity` | Validation Error | Schema validation failures |
| `500 Internal Server Error` | Server Error | Unexpected server issues |

### Error Response Format
```json
{
  "detail": "Error message description",
  "error_code": "VALIDATION_ERROR",
  "timestamp": "2024-01-01T12:00:00Z"
}
```

## 📁 Project Structure

```
zenstore-ai/
├── app/
│   ├── api/                    # API routes and dependencies
│   │   ├── auth.py            # Authentication endpoints
│   │   ├── products.py        # Product management endpoints
│   │   └── dependencies.py    # Common dependencies (auth, etc.)
│   ├── core/                   # Core application components
│   │   ├── config.py          # Configuration management
│   │   ├── database.py        # Database connection and session
│   │   └── security.py        # Security utilities (JWT, hashing)
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── user.py            # User model definition
│   │   └── product.py         # Product model definition
│   ├── repositories/           # Data access layer
│   │   ├── base.py            # Base repository class
│   │   ├── user.py            # User repository
│   │   └── product.py         # Product repository
│   ├── schemas/                # Pydantic request/response schemas
│   │   ├── user.py            # User schemas
│   │   └── product.py         # Product schemas
│   ├── services/               # Business logic layer
│   │   ├── auth.py            # Authentication service
│   │   └── product.py         # Product service
│   ├── utils/                  # Utility functions and decorators
│   │   ├── cache.py           # Redis caching utilities
│   │   └── validators.py      # Custom validators
│   ├── workers/                # Celery background tasks
│   │   ├── celery_app.py      # Celery application configuration
│   │   └── tasks.py           # Background task definitions
│   └── main.py                 # FastAPI application entry point
├── tests/                      # Pytest test suite
│   ├── conftest.py            # Test configuration and fixtures
│   ├── test_auth.py           # Authentication tests
│   ├── test_products.py       # Product management tests
│   └── test_bulk_upload.py    # Bulk upload functionality tests
├── docs/                       # Documentation and design notes
│   ├── api_design.md          # API design specifications
│   └── architecture.md        # Architecture documentation
├── alembic/                    # Database migration files
│   ├── versions/              # Migration scripts
│   └── alembic.ini            # Alembic configuration
├── scripts/                    # Utility scripts
│   └── new_migration.sh       # Migration generation script
├── docker-compose.yml          # Multi-container orchestration
├── Dockerfile                  # Application container definition
├── .env.docker                 # Docker environment variables
├── requirements.txt            # Python dependencies
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore patterns
└── README.md                  # Project documentation
```

## 🐳 Docker Deployment

### Overview

Zenstore AI includes comprehensive Docker support for containerized deployment, enabling easy scaling and consistent environments across development, staging, and production.

### Container Architecture

```mermaid
graph TB
    subgraph "Docker Network"
        API[API Container]
        Worker[Worker Container]
        Redis[Redis Container]
        DB[PostgreSQL Container]
    end
    
    Client --> API
    API --> Redis
    API --> DB
    Worker --> Redis
    Worker --> DB
```

### Docker Configuration Files

- **`Dockerfile`** - Single-stage build for application container
- **`docker-compose.yml`** - Multi-container orchestration with service definitions
- **`.env.docker`** - Environment-specific configuration for containers

### Port Mapping (Host → Container)

| Service | Host Port | Container Port | Purpose |
|---------|-----------|----------------|---------|
| API Server | `9071` | `9071` | HTTP API endpoints |
| Redis | `6380` | `6379` | Caching and message broker |
| PostgreSQL | `5434` | `5432` | Primary database |
| Worker | N/A | N/A | Background task processing |

### Quick Start with Docker

#### 1. Environment Setup
```bash
# Edit .env.docker with your configuration
# .env.docker already exists with default values
```

#### 2. Build and Launch Services
```bash
# Build images and start all services
docker compose up -d --build

# View service status
docker compose ps

# Monitor logs
docker compose logs -f
```

#### 3. Database Initialization
```bash
# Apply database migrations
docker compose exec api python -m alembic upgrade head

# Create initial admin user (optional)
docker compose exec api python -c "
from app.core.database import get_db
from app.services.auth import AuthService
from app.schemas.user import UserCreate
db = next(get_db())
auth_service = AuthService(db)
user = UserCreate(email='admin@example.com', password='admin123')
auth_service.create_user(user)
"
```

#### 4. Verify Deployment
```bash
# Health check
curl http://127.0.0.1:9071/health

# API documentation
open http://127.0.0.1:9071/docs

# Redis connection test
docker compose exec redis redis-cli ping
```

### Production Docker Environment

#### Environment Configuration
```env
# .env.docker - Production settings
DATABASE_URL=postgresql://postgres:postgres@db:5432/zenstore
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-prod-secret-key-32chars
AI_PROVIDER=groq
AI_MODEL=llama-3.1-8b-instant
GROQ_API_KEY=your-key-here
OPENAI_API_KEY=
OPENAI_BASE_URL=https://api.openai.com/v1
```

### Docker Operations

#### Service Management
```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# Force rebuild
docker compose up -d --build --force-recreate

# Scale services
docker compose up -d --scale worker=3 --scale api=2
```

#### Monitoring and Debugging
```bash
# View logs for all services
docker compose logs -f

# View logs for specific service
docker compose logs -f api

# Execute commands in container
docker compose exec api bash
docker compose exec worker python -c "import celery; print(celery.version)"

# Monitor resource usage
docker stats
```

#### Database Operations
```bash
# Database backup
docker compose exec db pg_dump -U postgres zenstore > backup.sql

# Database restore
docker compose exec -T db psql -U postgres zenstore < backup.sql

# Access database shell
docker compose exec db psql -U postgres zenstore

# Check database connections
docker compose exec api python -c "
from app.core.database import engine
print('Database connection:', engine.url)
"
```

#### Maintenance Tasks
```bash
# Clean up unused resources
docker system prune -f

# Remove all containers and volumes
docker compose down -v

# Update images
docker compose pull
docker compose up -d

# View disk usage
docker system df
```

### Development Docker Workflow

#### Testing in Docker
```bash
# Run test suite in container
docker compose exec api pytest

# Run specific test
docker compose exec api pytest tests/test_auth.py -v

# Generate coverage report
docker compose exec api pytest --cov=app --cov-report=html
```

### Security Considerations

- **Use secrets management** for sensitive configuration
- **Enable TLS** for production deployments
- **Implement network policies** to restrict container communication
- **Use non-root users** within containers
- **Implement resource limits** to prevent DoS attacks

### Troubleshooting Docker Issues

#### Common Problems
```bash
# Container won't start
docker compose logs api

# Database connection issues
docker compose exec db pg_isready

# Redis connection issues
docker compose exec redis redis-cli ping

# Worker not processing tasks
docker compose exec worker celery -A app.workers.celery_app.celery_app inspect active
```

## 🗃️ Database Migrations

### Overview

Zenstore AI uses **Alembic** for database schema management, providing version control for your database structure and enabling safe, reversible migrations.

### Migration Workflow

```mermaid
graph LR
    A[Code Changes] --> B[Create Migration]
    B --> C[Review Migration]
    C --> D[Apply Migration]
    D --> E[Verify Schema]
    E --> F[Update Tests]
```

### Migration Commands

#### Create New Migration
```bash
# Using the convenience script
./scripts/new_migration.sh "add user account deactivations"

# Or directly with Alembic
alembic revision --autogenerate -m "add user account deactivations"
```

#### Apply Migrations
```bash
# Apply all pending migrations
alembic upgrade head

# Apply to specific version
alembic upgrade +1

# Apply in Docker
docker compose exec api alembic upgrade head
```

#### Rollback Migrations
```bash
# Rollback one migration
alembic downgrade -1

# Rollback to specific version
alembic downgrade base

# Rollback in Docker
docker compose exec api alembic downgrade -1
```

#### Migration Management
```bash
# View current revision
alembic current

# View migration history
alembic history

# View pending migrations
alembic heads

# Check for model changes
alembic check
```

### Migration Best Practices

- **Review generated migrations** before applying
- **Test migrations** on development environment first
- **Backup database** before major migrations
- **Use descriptive migration messages**
- **Keep migrations atomic** and reversible
- **Test rollback procedures** regularly

## 🧪 Testing Strategy

### Testing Philosophy

Zenstore AI implements a **comprehensive testing strategy** with multiple test types to ensure reliability, security, and performance.

### Test Suite Structure

```mermaid
graph TB
    subgraph "Test Suite"
        Unit[Unit Tests]
        API[API Endpoint Tests]
        Functional[Functional Tests]
    end
    
    Unit --> API
    API --> Functional
    
    subgraph "Test Categories"
        Auth[Authentication Tests]
        API[API Endpoint Tests]
        Service[Service Logic Tests]
        DB[Database Tests]
        Performance[Performance Tests]
    end
```

### Running Tests

#### Full Test Suite
```bash
# Run all tests with coverage
pytest --cov=app --cov-report=html --cov-report=term

# Run tests in Docker
docker compose exec api pytest --cov=app

# Run tests with verbose output
pytest -v --tb=short
```

#### Specific Test Categories
```bash
# Authentication tests
pytest tests/test_auth.py -v

# Product management tests
pytest tests/test_products.py -v

# Bulk upload tests
pytest tests/test_bulk_upload.py -v

# Service layer tests
pytest tests/test_services/ -v
```

#### Test Configuration
```bash
# Run with specific database
pytest --test-db-url=sqlite:///./test.db

# Run with performance profiling
pytest --profile

# Run with debug output
pytest -s --log-cli-level=DEBUG
```

### Testing Architecture

#### Test Fixtures (`tests/conftest.py`)
```python
# Core fixtures provided:
- client: FastAPI TestClient
- db_session: Isolated database session
- auth_headers: Valid JWT authentication headers
- test_user: Pre-configured test user
- sample_products: Test product data
```

#### Test Database Strategy
- **Isolated SQLite database** for each test run
- **Schema recreation** between tests for deterministic results
- **Transaction rollback** for test isolation
- **Factory pattern** for test data generation

### Test Coverage Areas
- **Authentication Flow**: Registration, login, token validation
- **Authorization**: User permissions, resource ownership
- **API Contracts**: Request/response validation
- **Business Logic**: Service layer functionality
- **Data Integrity**: Repository layer operations
- **Error Handling**: Exception scenarios and edge cases

### Test Types and Examples

#### Unit Tests
```python
# Example: Service layer unit test
def test_product_creation_service(product_service, sample_product):
    result = product_service.create_product(sample_product)
    assert result.name == sample_product.name
    assert result.id is not None
```

#### API Endpoint Tests
```python
# Example: API endpoint test
def test_create_product_api(client, auth_headers, product_payload):
    response = client.post(
        "/products", 
        json=product_payload,
        headers=auth_headers
    )
    assert response.status_code == 202
```

#### Functional Tests
```python
# Example: Complete workflow test
def test_bulk_upload_workflow(client, auth_headers, csv_file):
    # Upload CSV
    response = client.post(
        "/products/bulk",
        files={"file": csv_file},
        headers=auth_headers
    )
    assert response.status_code == 202
    
    # Verify database state
    # Verify cache population
```

## 🚀 Operations & Deployment

### Production Deployment

#### Environment Setup
```bash
# Production environment variables
export DATABASE_URL="postgresql://user:pass@host:5432/zenstore_prod"
export REDIS_URL="redis://redis:6379/0"
export SECRET_KEY="your-production-secret-key-32-chars"
export LOG_LEVEL="INFO"
export WORKERS=4
```

#### Service Management
```bash
# Start API server with uvicorn
uvicorn app.main:app --host 0.0.0.0 --port 9072 --workers 4

# Start Celery worker
celery -A app.workers.celery_app.celery_app worker --loglevel=info --concurrency=4
```

### Scaling Considerations

#### Horizontal Scaling
- **API Servers**: Multiple instances for high availability
- **Workers**: Scale based on task queue length
- **Redis**: Cluster for high availability

### Security Operations

#### Security Checklist
- ✅ **Strong JWT secrets** (32+ characters)
- ✅ **HTTPS/TLS** in production
- ✅ **Rate limiting** on API endpoints
- ✅ **Input validation** and sanitization
- ✅ **SQL injection prevention** via ORM
- ✅ **CORS configuration** for web clients
- ✅ **Security headers** (HSTS, CSP, etc.)

#### Security Monitoring
```bash
# Monitor failed authentication attempts
grep "Failed login" /var/log/zenstore/api.log

# Monitor suspicious API activity
tail -f /var/log/zenstore/api.log | grep "401\|403\|429"

# Database access monitoring
docker compose exec db psql -U postgres zenstore -c "
SELECT * FROM pg_stat_activity WHERE state = 'active';
"
```

## 🔧 Troubleshooting Guide

### Common Issues and Solutions

#### Authentication Problems
```bash
# Issue: JWT token validation failures
# Solution: Check SECRET_KEY length and format
echo $SECRET_KEY | wc -c  # Should be 32+ characters

# Issue: Token expiration
# Solution: Check token expiration time
python -c "
import jwt
token = 'your-token-here'
print(jwt.decode(token, options={'verify_signature': False}))
"
```

#### Database Connection Issues
```bash
# Check database connectivity
docker compose exec db pg_isready

# Test connection from application
docker compose exec api python -c "
from app.core.database import engine
try:
    with engine.connect() as conn:
        print('Database connection successful')
except Exception as e:
    print(f'Database error: {e}')
"

# Check connection pool status
docker compose exec api python -c "
from app.core.database import engine
print(f'Pool size: {engine.pool.size()}')
print(f'Checked out: {engine.pool.checkedout()}')
"
```

#### Redis Connection Issues
```bash
# Test Redis connectivity
docker compose exec redis redis-cli ping

# Check Redis memory usage
docker compose exec redis redis-cli info memory

# Monitor Redis operations
docker compose exec redis redis-cli monitor
```

#### Celery Worker Issues
```bash
# Check worker status
celery -A app.workers.celery_app.celery_app inspect active

# Monitor worker logs
docker compose logs -f worker

# Check task queue length
celery -A app.workers.celery_app.celery_app inspect reserved

# Restart stuck workers
docker compose restart worker
```

#### Performance Issues
```bash
# Monitor system resources
docker stats

# Check database query performance
docker compose exec db psql -U postgres zenstore -c "
SELECT query, mean_time, calls, total_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;
"

# Profile application performance
python -m cProfile -o profile.stats -m uvicorn app.main:app
```

### Debug Mode

#### Enable Debug Logging
```bash
# Set debug environment
export LOG_LEVEL=DEBUG
export DEBUG=true

# Run with debug output
uvicorn app.main:app --log-level debug --reload
```

#### Database Debugging
```bash
# Enable SQL query logging
export SQL_ECHO=true

# Run with query logging
uvicorn app.main:app --log-level debug
```

## 📄 License

**Zenstore AI** is an internal project developed for production use.

© 2024 Zenstore AI. All rights reserved.

---

## 🤝 Contributing

### Development Guidelines

1. **Code Quality**: Follow PEP 8 and use type hints
2. **Testing**: Maintain >90% test coverage
3. **Documentation**: Update README and API docs
4. **Security**: Follow security best practices
5. **Performance**: Profile and optimize critical paths

### Submitting Changes

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Code Review Process

- Automated tests must pass
- Code coverage maintained
- Security review completed
- Documentation updated
- Performance impact assessed

---

## 📞 Support

For technical support and questions:

- **Documentation**: Check this README and `/docs` endpoint
- **Issues**: Create GitHub issues for bugs and feature requests
- **Discussions**: Use GitHub Discussions for questions
- **Email**: Contact the development team for urgent matters

---

*Last updated: January 2024*
