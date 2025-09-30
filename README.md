# MemoryVault

A production-grade AI-powered platform to preserve life stories for future generations.

## Problem Statement

70% of family stories are lost within two generations. MemoryVault solves this by creating an AI interviewer that empathetically captures and preserves the life stories of our elders in their own voices.

## Architecture Overview

MemoryVault is built as a modern monorepo application:

```
┌─────────────────┐
│   Next.js App   │  (Frontend)
│   TypeScript    │
└────────┬────────┘
         │
    REST API
         │
┌────────┴────────┐
│  FastAPI Server │  (Backend)
│     Python      │
└────────┬────────┘
         │
    ┌────┴─────┬──────────┬───────────┐
    │          │          │           │
┌───┴───┐ ┌───┴────┐ ┌──┴─────┐ ┌───┴────┐
│ PostgreSQL│ │  IPFS   │ │ OpenAI  │ │ ElevenLabs│
│ Database  │ │ Storage │ │   AI    │ │   Voice   │
└───────────┘ └─────────┘ └─────────┘ └──────────┘
```

## Tech Stack

### Backend
- **FastAPI** - Modern, fast Python web framework with auto-generated API docs
- **PostgreSQL** - Reliable relational database with JSONB support
- **SQLAlchemy** - ORM with async support
- **Alembic** - Database migrations
- **Celery/ARQ** - Background task processing

### Frontend
- **Next.js 14** - React framework with App Router and SSR
- **TypeScript** - Type safety and better DX
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Beautiful, accessible component library
- **Zustand** - Lightweight state management

### AI & Storage
- **OpenAI GPT-4** - AI interviewer and content enrichment
- **Whisper API** - Audio transcription
- **ElevenLabs** - Voice cloning and synthesis
- **Pinata IPFS** - Permanent, decentralized storage for memories

### Why These Choices?

1. **FastAPI** - Async support, automatic documentation, Python's rich AI ecosystem
2. **Next.js** - SEO-friendly SSR, excellent DX, production-ready out of the box
3. **IPFS** - Families truly own their data, permanent storage, marketing differentiator
4. **OpenAI** - Best-in-class conversation quality and transcription accuracy

## Development Setup

### Prerequisites
- Node.js >= 18
- Python >= 3.11
- pnpm >= 8
- Docker and Docker Compose
- PostgreSQL 15+

### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd memvault
```

2. Install dependencies:
```bash
pnpm install
cd packages/backend && pip install -r requirements/dev.txt
```

3. Set up environment variables:
```bash
cp packages/backend/.env.example packages/backend/.env
cp packages/frontend/.env.local.example packages/frontend/.env.local
```

4. Start development services:
```bash
docker-compose up -d  # Start PostgreSQL and Redis
cd packages/backend && alembic upgrade head  # Run migrations
```

5. Run the development servers:
```bash
pnpm dev  # Starts both backend and frontend
```

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Project Structure

```
memvault/
├── packages/
│   ├── backend/          # FastAPI application
│   │   ├── app/
│   │   │   ├── api/      # API endpoints
│   │   │   ├── core/     # Config, security, logging
│   │   │   ├── db/       # Database models and session
│   │   │   ├── services/ # Business logic
│   │   │   ├── schemas/  # Pydantic models
│   │   │   └── utils/    # Utilities
│   │   ├── alembic/      # Database migrations
│   │   ├── tests/        # Backend tests
│   │   └── requirements/ # Python dependencies
│   └── frontend/         # Next.js application
│       ├── src/
│       │   ├── app/      # Pages and layouts
│       │   ├── components/ # React components
│       │   ├── lib/      # Utilities and API client
│       │   └── types/    # TypeScript types
│       └── tests/        # Frontend tests
├── shared/               # Shared types and constants
├── docs/                 # Documentation
└── .github/              # CI/CD workflows
```

## Key Features

### Current
- Elder profile management
- Memory capture and storage
- AI-powered interviewer
- Audio transcription
- Family dashboard

### Planned
- Voice cloning for elders
- Interactive timeline visualization
- Advanced search and filtering
- Memory export (PDF, audio book)
- Family collaboration features

## Contributing

This is a personal project, but contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Development Workflow

1. Create a feature branch
2. Make your changes
3. Run tests: `pnpm test`
4. Run linting: `pnpm lint`
5. Commit with conventional commits
6. Push and create a PR

## License

MIT License - see [LICENSE](LICENSE) for details

## Contact

For questions or feedback, please open an issue on GitHub.
