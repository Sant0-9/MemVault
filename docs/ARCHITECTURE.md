# MemoryVault Architecture

## System Overview

MemoryVault is a full-stack application built as a monorepo with separate frontend and backend packages.

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────┐
│                    Client Layer                           │
│  ┌────────────────────────────────────────────────────┐  │
│  │   Next.js 14 Frontend (TypeScript)                 │  │
│  │   - Server-side rendering                          │  │
│  │   - Client-side routing                            │  │
│  │   - State management (Zustand)                     │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
                           │
                    REST API (HTTPS)
                           │
┌──────────────────────────────────────────────────────────┐
│                   API Gateway Layer                       │
│  ┌────────────────────────────────────────────────────┐  │
│  │   FastAPI Backend (Python)                         │  │
│  │   - API versioning (/api/v1)                       │  │
│  │   - Authentication & Authorization                 │  │
│  │   - Request validation                             │  │
│  │   - Rate limiting                                  │  │
│  └────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
┌───────▼────────┐  ┌──────▼──────┐  ┌───────▼────────┐
│  Business      │  │  Background  │  │   AI Services  │
│  Logic         │  │  Tasks       │  │                │
│  - Services    │  │  - Celery    │  │  - OpenAI      │
│  - Validation  │  │  - Redis     │  │  - Whisper     │
│  - Workflows   │  │  Queue       │  │  - ElevenLabs  │
└───────┬────────┘  └──────┬──────┘  └───────┬────────┘
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
┌──────────────────────────────────────────────────────────┐
│                    Data Layer                             │
│  ┌────────────┐  ┌────────────┐  ┌────────────────────┐ │
│  │ PostgreSQL │  │   Redis    │  │   IPFS (Pinata)    │ │
│  │ - Relational│  │   - Cache  │  │   - Audio storage  │ │
│  │   data     │  │   - Sessions│  │   - Permanent data │ │
│  │ - Full-text│  │   - Queue  │  │   - Decentralized  │ │
│  └────────────┘  └────────────┘  └────────────────────┘ │
└──────────────────────────────────────────────────────────┘
```

## Technology Stack

### Frontend
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: Zustand
- **API Client**: Axios

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **ORM**: SQLAlchemy (async)
- **Migrations**: Alembic
- **Tasks**: Celery

### Data Storage
- **Primary Database**: PostgreSQL 15
- **Cache/Queue**: Redis
- **File Storage**: IPFS via Pinata
- **Search**: PostgreSQL full-text search

### AI & ML
- **Conversation**: OpenAI GPT-4
- **Transcription**: OpenAI Whisper
- **Voice Cloning**: ElevenLabs
- **NLP**: spaCy

## Directory Structure

```
memvault/
├── packages/
│   ├── backend/              # FastAPI backend
│   │   ├── app/
│   │   │   ├── api/          # API endpoints
│   │   │   ├── core/         # Core config
│   │   │   ├── db/           # Database
│   │   │   ├── services/     # Business logic
│   │   │   └── schemas/      # Pydantic models
│   │   ├── alembic/          # Migrations
│   │   └── tests/            # Tests
│   └── frontend/             # Next.js frontend
│       ├── src/
│       │   ├── app/          # Pages
│       │   ├── components/   # React components
│       │   └── lib/          # Utilities
│       └── tests/            # Tests
├── shared/                   # Shared code
│   ├── types/               # TypeScript types
│   ├── constants/           # Constants
│   └── utils/               # Utilities
└── docs/                    # Documentation
```

## Key Design Decisions

### 1. Monorepo Structure
- Shared types between frontend and backend
- Consistent tooling across packages
- Simplified dependency management

### 2. Async-First Backend
- FastAPI with async/await
- AsyncPG for PostgreSQL
- Better performance for I/O-bound operations

### 3. Background Job Processing
- Celery for long-running tasks
- Audio processing, transcription, enrichment
- Redis as message broker

### 4. IPFS for Storage
- Permanent, decentralized storage
- Families own their data
- Marketing differentiator

### 5. API Versioning
- All endpoints under /api/v1
- Future-proof for breaking changes
- Backward compatibility

## Data Flow

### Memory Creation Flow
1. User uploads audio file
2. File validated and stored temporarily
3. Background job created
4. Audio transcribed (Whisper API)
5. Transcription enriched (GPT-4)
6. Audio uploaded to IPFS
7. Memory saved to database
8. User notified of completion

### AI Interview Flow
1. User starts interview session
2. AI generates opening question
3. User responds (audio recorded)
4. Audio transcribed in real-time
5. AI analyzes response
6. AI generates follow-up question
7. Loop continues until session end
8. Memories created from session

## Security Considerations

- JWT-based authentication
- Rate limiting on API endpoints
- Input validation at all layers
- SQL injection prevention (ORM)
- XSS prevention (React escaping)
- CORS configured by environment
- Secrets managed via environment variables

## Scalability

### Current Architecture
- Single server deployment
- PostgreSQL on same server
- Redis for caching and queue

### Future Scaling
- Horizontal scaling with load balancer
- Database read replicas
- CDN for static assets
- Separate Celery workers
- Queue-based architecture

## Monitoring & Observability

### Planned Integration
- Sentry for error tracking
- Structured logging (JSON)
- Request ID tracing
- Performance metrics
- Health check endpoints
