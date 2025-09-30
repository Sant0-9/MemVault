# Development Guide

## Prerequisites

- Node.js >= 18
- Python >= 3.11
- pnpm >= 8
- Docker and Docker Compose
- PostgreSQL 15+ (if running locally)
- Redis (if running locally)

## Initial Setup

### 1. Clone and Install

```bash
git clone <repository-url>
cd memvault
pnpm install
```

### 2. Backend Setup

```bash
cd packages/backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/dev.txt

# Copy environment file
cp .env.example .env

# Update .env with your API keys
```

### 3. Frontend Setup

```bash
cd packages/frontend

# Copy environment file
cp .env.local.example .env.local

# Update .env.local with your configuration
```

### 4. Start Development Services

```bash
# From project root
docker-compose up -d postgres redis

# Wait for services to be healthy
docker-compose ps
```

### 5. Run Database Migrations

```bash
cd packages/backend
alembic upgrade head
```

## Running the Application

### Option 1: Run Both Services with pnpm

```bash
# From project root
pnpm dev
```

This starts:
- Backend: http://localhost:8000
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/api/v1/docs

### Option 2: Run Services Separately

**Backend:**
```bash
cd packages/backend
make dev
# or
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd packages/frontend
pnpm dev
```

### Option 3: Run Everything in Docker

```bash
docker-compose up
```

## Development Workflow

### Making Changes

1. Create a feature branch
2. Make your changes
3. Run tests
4. Commit with conventional commits
5. Push and create PR

### Backend Development

#### Run Tests
```bash
cd packages/backend
make test
# or
pytest -v
```

#### Run Linters
```bash
make lint
# or individually:
black app/
isort app/
mypy app/
pylint app/
```

#### Format Code
```bash
make format
```

#### Create Migration
```bash
alembic revision --autogenerate -m "description"
```

#### Apply Migration
```bash
alembic upgrade head
```

#### Rollback Migration
```bash
alembic downgrade -1
```

### Frontend Development

#### Run Tests
```bash
cd packages/frontend
pnpm test
```

#### Run Linter
```bash
pnpm lint
```

#### Type Check
```bash
pnpm type-check
```

#### Format Code
```bash
pnpm format
```

## Common Tasks

### Adding a New API Endpoint

1. Create endpoint in `packages/backend/app/api/v1/endpoints/`
2. Add route to `packages/backend/app/api/v1/api.py`
3. Create Pydantic schemas in `packages/backend/app/schemas/`
4. Add business logic in `packages/backend/app/services/`
5. Write tests in `packages/backend/tests/`

### Adding a New Page

1. Create page in `packages/frontend/src/app/`
2. Add components in `packages/frontend/src/components/`
3. Add API calls in `packages/frontend/src/lib/`
4. Update types in `shared/types/`

### Working with Database

```bash
# Connect to PostgreSQL
docker exec -it memvault-postgres psql -U postgres -d memvault

# Backup database
docker exec memvault-postgres pg_dump -U postgres memvault > backup.sql

# Restore database
docker exec -i memvault-postgres psql -U postgres memvault < backup.sql
```

### Working with Redis

```bash
# Connect to Redis
docker exec -it memvault-redis redis-cli

# Clear cache
docker exec -it memvault-redis redis-cli FLUSHDB
```

## Environment Variables

### Backend (.env)

Required:
- `SECRET_KEY` - JWT secret key
- `DATABASE_URL` - PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key

Optional:
- `ELEVENLABS_API_KEY` - For voice cloning
- `PINATA_API_KEY` - For IPFS storage
- `SENDGRID_API_KEY` - For email notifications

### Frontend (.env.local)

Required:
- `NEXT_PUBLIC_API_URL` - Backend API URL

Optional:
- `NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY` - If using Clerk
- `CLERK_SECRET_KEY` - If using Clerk

## Debugging

### Backend

```bash
# Run with debugger
python -m pdb app/main.py

# View logs
docker-compose logs -f backend
```

### Frontend

```bash
# View logs
docker-compose logs -f frontend

# Enable debug mode in browser DevTools
```

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# Restart PostgreSQL
docker-compose restart postgres

# View logs
docker-compose logs postgres
```

### Port Already in Use

```bash
# Find process using port
lsof -i :8000  # or :3000

# Kill process
kill -9 <PID>
```

### Module Not Found

```bash
# Backend
cd packages/backend
pip install -r requirements/dev.txt

# Frontend
cd packages/frontend
pnpm install
```

## Performance Tips

1. Use `--reload` only in development
2. Enable caching in Redis
3. Use database indexes
4. Optimize queries with EXPLAIN
5. Use CDN for static assets

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Next.js Documentation](https://nextjs.org/docs)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
