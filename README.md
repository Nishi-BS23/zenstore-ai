# Zenstore AI

**Zenstore AI** is an enterprise-grade, production-ready FastAPI backend system designed for modern e-commerce and product management platforms. It delivers a comprehensive solution for authenticated product management, intelligent AI-powered content enrichment, scalable bulk data ingestion, and high-performance Redis-backed caching.

Built with a focus on **scalability**, **security**, and **maintainability**, the system implements a clean, layered architecture that separates concerns and ensures operational excellence in production environments.

## 🚀 Core Features

### Authentication & Security
- **JWT-based authentication** with bcrypt password hashing for secure user management
- **Role-based access control** with owner-scoped product operations
- **Secure session management** with configurable token expiration

### Product Management
- **RESTful CRUD APIs** for product listing and single addition
- **Owner-scoped data isolation** ensuring user data privacy
- **Real-time validation** and robust error handling

### AI-Powered Enrichment
- **Asynchronous AI content generation** via Celery task queue (non-blocking)
- **Free API integration** (Groq, OpenAI) for LLM-powered content transformation
- **Catchy 2-sentence product descriptions** automatically generated from product names
- **Intelligent category classification** based on product characteristics

### Data Processing & Storage
- **High-performance CSV bulk ingestion** with streaming row processing
- **Cache-aside Redis strategy** for optimal read performance
- **Repository pattern implementation** for consistent data access
- **Python Generators** for efficient batch file processing

### Testing & Quality Assurance
- **Comprehensive pytest suite** with isolated SQLite test database
- **Automated test fixtures** and deterministic test results
- **API contract testing** with full coverage validation

### Technical Implementation
- **OOP Principles** with clean layered architecture
- **Custom Decorator** for performance logging
- **Python Generators** for efficient batch file processing
- **Caching Layer** with Redis for optimal performance
- **JWT Authentication** for secure user data isolation
- **Swagger Documentation** for API testing

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
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

## Health Check

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

© 2026 Zenstore AI. All rights reserved.

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

*Last updated: January 2026*
