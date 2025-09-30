# Contributing to MemoryVault

Thank you for your interest in contributing to MemoryVault.

## Development Setup

1. Fork and clone the repository
2. Install dependencies:
   ```bash
   pnpm install
   cd packages/backend && pip install -r requirements/dev.txt
   ```
3. Copy environment files:
   ```bash
   cp packages/backend/.env.example packages/backend/.env
   cp packages/frontend/.env.local.example packages/frontend/.env.local
   ```
4. Start development services:
   ```bash
   docker-compose up -d
   cd packages/backend && alembic upgrade head
   ```

## Development Workflow

1. Create a feature branch from `develop`
2. Make your changes
3. Run tests and linters
4. Commit with conventional commits
5. Push and create a PR

## Code Standards

### Backend (Python)
- Follow PEP 8 style guide
- Use type hints
- Write docstrings for functions
- Maintain test coverage above 80%

### Frontend (TypeScript)
- Use functional components with hooks
- Follow TypeScript strict mode
- Use Tailwind CSS for styling
- Write meaningful component names

## Commit Messages

Use conventional commits:
- `feat: add new feature`
- `fix: bug fix`
- `docs: documentation update`
- `style: formatting changes`
- `refactor: code refactoring`
- `test: add tests`
- `chore: maintenance tasks`

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure CI passes
4. Request review from maintainers
5. Address review feedback

## Questions?

Open an issue for any questions or concerns.
