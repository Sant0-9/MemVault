# MemoryVault - Complete Development Guide for Claude Code

**A Production-Grade Personal Project**  
*Build a meaningful AI-powered platform to preserve life stories for future generations*

---

## 🎯 PROJECT VISION

MemoryVault is your passion project to solve a real problem: **70% of family stories are lost within two generations**. This isn't a weekend hack—it's a carefully crafted product that you'll be proud to show employers, use with your own family, and potentially turn into a startup.

**Target Outcome:**
- Production-ready SaaS application
- Portfolio centerpiece that demonstrates your full-stack + AI expertise
- Potential revenue-generating side project
- Something that genuinely helps families preserve memories

---

## 📅 DEVELOPMENT TIMELINE (8-12 Weeks)

### Phase 1: Foundation (Weeks 1-2)
- Project setup & architecture
- Database design & migrations
- Core API infrastructure
- Basic authentication

### Phase 2: Core Features (Weeks 3-5)
- AI interviewer system
- Voice/audio processing pipeline
- Memory storage (IPFS)
- Family dashboard MVP

### Phase 3: Advanced Features (Weeks 6-8)
- Voice cloning
- Timeline visualization
- Search & analytics
- Export features

### Phase 4: Polish & Launch (Weeks 9-12)
- UI/UX refinement
- Performance optimization
- Testing & bug fixes
- Documentation & deployment
- Marketing landing page

---

## 🏗️ ARCHITECTURE DECISIONS

### Why These Technologies?

**Backend: FastAPI + PostgreSQL**
- FastAPI: Modern, fast, auto-generated API docs, async support
- PostgreSQL: Reliable, powerful querying, JSONB for flexible data
- Alternative: Django if you prefer batteries-included

**Frontend: Next.js 14 + TypeScript**
- Server-side rendering for SEO
- Type safety reduces bugs
- Great developer experience
- Alternative: SvelteKit if you want something lighter

**AI: OpenAI APIs + ElevenLabs**
- GPT-4: Best conversation quality
- Whisper: Industry-leading transcription
- ElevenLabs: Highest quality voice cloning
- Cost: ~$50-100/month for moderate usage

**Storage: Pinata IPFS**
- Permanent, decentralized storage
- Family truly owns their data
- Marketing angle: "Your memories can never be deleted by a company"
- Alternative: AWS S3 + CloudFront if you want traditional approach

---

## 📋 PHASE 1: FOUNDATION (WEEKS 1-2)

### WEEK 1: Project Setup & Database

#### Prompt 1.1: Initialize Monorepo Structure

```
Create a production-grade monorepo for "MemoryVault" with the following structure:

Project Root:
- Use pnpm workspaces or npm workspaces
- Create packages/backend and packages/frontend
- Create shared/ folder for shared types and utilities
- Add .github/workflows/ for CI/CD
- Create comprehensive .gitignore
- Add LICENSE (MIT)
- Create detailed README.md with:
  - Project vision and problem statement
  - Architecture overview diagram
  - Tech stack justification
  - Development setup instructions
  - Contribution guidelines

Backend (packages/backend):
- FastAPI application with best practices
- Folder structure:
  - app/
    - api/v1/endpoints/ (instead of routes)
    - core/ (config, security, logging)
    - db/ (models, session, migrations)
    - services/ (business logic)
    - schemas/ (Pydantic models)
    - utils/
    - tests/
  - alembic/ (migrations)
  - scripts/ (utility scripts)
- requirements/
  - base.txt (production dependencies)
  - dev.txt (development dependencies)
  - test.txt (testing dependencies)
- Dockerfile (multi-stage build)
- docker-compose.yml (local development with PostgreSQL, Redis)
- pytest.ini
- .env.example with all required variables
- Makefile for common tasks (run, test, migrate, format)

Frontend (packages/frontend):
- Next.js 14 with App Router and TypeScript
- Folder structure:
  - src/
    - app/ (pages)
    - components/
      - ui/ (shadcn/ui components)
      - features/ (feature-specific components)
      - layouts/
    - lib/ (utilities, API client, hooks)
    - stores/ (Zustand stores)
    - types/
    - styles/
  - public/ (static assets)
  - tests/
- package.json with organized scripts
- tsconfig.json (strict mode)
- tailwind.config.ts (with custom theme)
- next.config.js
- .env.local.example
- vitest.config.ts for testing

Shared (shared/):
- types/ (TypeScript types used by both frontend and backend)
- constants/
- utils/

Documentation (docs/):
- ARCHITECTURE.md
- API.md
- DEVELOPMENT.md
- DEPLOYMENT.md
- TESTING.md
- CONTRIBUTING.md

Include:
- Pre-commit hooks (husky) for linting and formatting
- ESLint + Prettier configuration
- Python: black, isort, mypy, pylint
- GitHub Actions for CI (lint, test, type-check)
```

#### Prompt 1.2: Database Design & Setup

```
Design and implement a robust PostgreSQL database for MemoryVault:

1. Create comprehensive database models in app/db/models/:

elder.py:
- Enhanced Elder model with:
  - Personal info (name, DOB, hometown, current_location)
  - Contact (phone, email, emergency_contact)
  - Profile (photo_url, bio, personality_traits JSONB)
  - Voice (voice_profile_id for ElevenLabs, sample_audios JSONB)
  - Preferences (preferred_language, interview_frequency, privacy_settings JSONB)
  - Metadata (created_at, updated_at, last_active_at, is_active)
  - Soft delete support (deleted_at)

memory.py:
- Comprehensive Memory model with:
  - Content (title, transcription, summary, full_text)
  - Media (audio_url, audio_cid, duration_seconds, waveform_data JSONB)
  - Classification (category, subcategory, era, decade)
  - Context (location, date_of_event, people_mentioned JSONB)
  - AI Analysis (tags JSONB, entities JSONB, sentiment, emotional_tone)
  - Enrichment (historical_context, related_events JSONB)
  - Engagement (play_count, share_count, favorite_by JSONB)
  - Privacy (is_private, is_sensitive, content_warnings JSONB)
  - Quality (transcription_confidence, audio_quality_score)
  - Timestamps (recorded_at, created_at, updated_at)
  - Full-text search support (tsvector column)

family_member.py:
- Detailed FamilyMember model with:
  - Identity (user_id from auth provider, name, email, phone)
  - Relationship (relationship_type, custom_relationship_label)
  - Permissions (access_level, specific_permissions JSONB)
  - Preferences (notification_settings JSONB, language)
  - Activity (last_login_at, total_time_spent, memories_listened)
  - Soft delete support

interview_session.py:
- Comprehensive InterviewSession model with:
  - Session info (elder_id, interviewer_id, session_type)
  - Timing (started_at, ended_at, total_duration, pause_duration)
  - Content (questions_asked JSONB, conversation_log JSONB)
  - Quality (completeness_score, engagement_score, interruption_count)
  - Outcomes (memories_created, follow_up_questions JSONB)
  - AI Metrics (mood_progression JSONB, fatigue_indicators JSONB)
  - Notes (interviewer_notes, system_notes)

question.py:
- Question bank model:
  - Content (text, category, subcategory, follow_up_templates JSONB)
  - Targeting (difficulty_level, recommended_age_range, cultural_context)
  - Effectiveness (usage_count, avg_response_quality, avg_response_length)
  - Safety (trigger_warnings JSONB, sensitivity_level)
  - Customization (variations JSONB, conditional_display JSONB)

notification.py:
- Notification system:
  - Recipient (family_member_id), type, priority
  - Content (title, message, action_url, data JSONB)
  - Status (is_read, read_at, is_dismissed)

memory_export.py:
- Export tracking:
  - Elder_id, format (pdf, audio, json)
  - Status, file_url, expires_at
  - Options (include_photos, include_audio, date_range)

2. Add database indexes for:
   - Frequently queried fields (elder_id, category, era, created_at)
   - Full-text search on memory transcriptions
   - JSONB fields that are filtered often

3. Create Alembic migrations with:
   - Initial schema
   - Seed data for question bank (50+ questions)
   - Sample categories and tags

4. Add database utility functions:
   - Connection pooling configuration
   - Transaction management helpers
   - Query performance logging
   - Automatic timestamps (updated_at)

5. Create app/db/session.py with:
   - Async database session management
   - Dependency injection for FastAPI
   - Connection pool configuration for production

6. Write comprehensive database tests:
   - Model validation
   - Relationship integrity
   - Cascade deletes
   - Constraint checks
```

#### Prompt 1.3: Core API Infrastructure

```
Build a production-grade FastAPI application infrastructure:

1. app/core/config.py:
   - Pydantic Settings for environment variables
   - Separate configs for dev/staging/production
   - Validation for all required variables
   - Type hints for everything
   - Secrets management best practices

2. app/core/security.py:
   - Password hashing with bcrypt
   - JWT token generation and verification
   - API key validation
   - Rate limiting configuration
   - CORS configuration by environment
   - CSP headers
   - Request ID middleware for tracing

3. app/core/logging.py:
   - Structured logging with Python's logging module
   - Log levels by environment
   - Request/response logging
   - Error tracking integration (Sentry placeholder)
   - Performance logging (slow query detection)
   - Log rotation configuration

4. app/main.py:
   - FastAPI app initialization with custom settings
   - Middleware stack:
     - CORS (environment-aware)
     - Request ID
     - Logging
     - Error handling
     - Rate limiting
     - Compression
   - Global exception handlers
   - Startup/shutdown events (DB connection, cleanup)
   - API versioning strategy (/api/v1/)
   - Health check endpoints:
     - GET /health (basic health)
     - GET /health/ready (DB connection, external services)
     - GET /health/live (application is running)
   - OpenAPI documentation customization
   - Admin-only endpoints protection

5. app/api/v1/api.py:
   - Central router that includes all endpoint routers
   - Organized by domain (elders, memories, interviews, etc.)

6. app/api/dependencies.py:
   - Common dependencies:
     - get_db (database session)
     - get_current_user (from JWT)
     - require_admin (role check)
     - rate_limit (per-endpoint limits)
     - pagination_params (page, size, sort)

7. app/schemas/base.py:
   - Base Pydantic models
   - Common response schemas (Success, Error, Paginated)
   - Shared field types (EmailStr, URLStr, etc.)

8. Error handling:
   - Custom exception classes
   - HTTP exception handlers
   - Validation error formatting
   - User-friendly error messages

9. Testing setup:
   - conftest.py with fixtures (test DB, client, auth)
   - Factory patterns for test data
   - Integration test examples
   - Async test support

10. Documentation:
    - API documentation in docs/API.md
    - Endpoint examples with curl commands
    - Authentication flow diagram
    - Error response catalog
```

### WEEK 2: Authentication & Basic CRUD

#### Prompt 1.4: Authentication System

```
Implement a complete authentication and authorization system:

1. Choose auth strategy:
   Option A: Self-hosted JWT auth
   Option B: Clerk integration (recommended for faster development)
   Option C: Supabase Auth integration

For Self-Hosted JWT:

app/core/auth.py:
- JWT token creation with configurable expiry
- Token refresh mechanism
- Password reset flow with secure tokens
- Email verification flow
- OAuth2 password bearer scheme

app/api/v1/endpoints/auth.py:
- POST /auth/register - User registration
- POST /auth/login - Login (returns access + refresh tokens)
- POST /auth/refresh - Refresh access token
- POST /auth/logout - Invalidate tokens
- POST /auth/forgot-password - Request password reset
- POST /auth/reset-password - Complete password reset
- POST /auth/verify-email - Verify email address
- GET /auth/me - Get current user info

app/services/email.py:
- Email sending service (SendGrid/Mailgun/AWS SES)
- Templates for:
  - Welcome email
  - Password reset
  - Email verification
  - New memory notification
  - Weekly digest

For Clerk Integration (Recommended):
- Install @clerk/fastapi
- Configure webhook endpoints for user sync
- Create app/services/clerk_service.py
- Sync Clerk users to local database
- Implement role-based access control on top of Clerk

2. Role-Based Access Control (RBAC):

app/models/user.py:
- User model with roles (admin, elder, family_member)
- Permission system

app/core/permissions.py:
- Permission decorators (@require_admin, @require_elder_access)
- Resource-level permissions (can_view_memory, can_edit_elder)
- Family relationship-based access

3. API Key authentication for external integrations:
- API key generation and management
- Scoped permissions for API keys
- Usage tracking and rate limiting per key

4. Security best practices:
- Password strength requirements
- Account lockout after failed attempts
- Session management
- Audit logging for sensitive operations
- GDPR compliance helpers (data export, deletion)

5. Frontend auth integration:
- Create lib/auth.ts with auth helpers
- Protected route middleware
- Auth context provider
- Login/register forms
- Password reset flow
```

#### Prompt 1.5: Elder & Memory CRUD APIs

```
Implement comprehensive CRUD operations for core resources:

1. app/api/v1/endpoints/elders.py:

Endpoints:
- POST /elders - Create elder profile
  - Request validation (name required, email format, phone format)
  - Duplicate check (phone/email)
  - Return created elder with ID
  
- GET /elders - List elders (with pagination, search, filters)
  - Query params: page, size, search, sort_by, order
  - Filter by: is_active, created_date_range
  - Response includes pagination metadata
  
- GET /elders/{elder_id} - Get elder details
  - Include related data: memory_count, family_member_count
  - Include voice_profile_status
  - Include last_interview_date
  
- PUT /elders/{elder_id} - Update elder
  - Partial updates supported
  - Validate changes
  - Track update history
  
- DELETE /elders/{elder_id} - Soft delete elder
  - Mark as deleted but keep data
  - Cascade to memories (soft delete)
  - Send notifications to family
  
- GET /elders/{elder_id}/stats - Get elder statistics
  - Total memories, total duration
  - Category breakdown
  - Timeline completeness
  - Engagement metrics

2. app/api/v1/endpoints/memories.py:

Endpoints:
- POST /memories - Create memory
  - Accept audio file upload or transcription
  - Optional: audio_url, transcription, metadata
  - Trigger background jobs: transcription, enrichment
  - Return memory with processing status
  
- GET /memories - List memories (advanced filtering)
  - Filter by: elder_id, category, era, emotion, date_range
  - Search: full-text search on transcription
  - Sort: date, duration, relevance
  - Pagination with cursors for large datasets
  
- GET /memories/{memory_id} - Get memory details
  - Include full transcription
  - Include enrichment data
  - Include engagement metrics
  - Include related memories (same category/era)
  
- PUT /memories/{memory_id} - Update memory
  - Update metadata, tags, privacy settings
  - Re-trigger enrichment if content changes
  
- DELETE /memories/{memory_id} - Delete memory
  - Soft delete
  - Remove from IPFS (optional)
  - Audit log the deletion
  
- POST /memories/{memory_id}/enrich - Manually trigger enrichment
  - Run AI analysis
  - Add historical context
  - Extract entities
  - Update tags
  
- GET /memories/search - Advanced search
  - Full-text search with ranking
  - Faceted search (by category, era, people)
  - Date range filters
  - Similar memories (vector similarity)

3. app/services/elder_service.py:
- Business logic for elder operations
- Validation rules
- Related data management
- Event dispatching (notifications)

4. app/services/memory_service.py:
- Memory lifecycle management
- Audio processing coordination
- Enrichment orchestration
- Search indexing

5. app/schemas/elder_schema.py & memory_schema.py:
- Request/response schemas for all operations
- Validation rules
- Examples for documentation

6. Implement soft delete pattern:
- Add deleted_at column to models
- Filter out deleted records by default
- Admin endpoint to permanently delete

7. Add comprehensive validation:
- File upload validation (size, format)
- Content moderation (for transcriptions)
- Duplicate detection
- Data consistency checks

8. Write integration tests:
- Test all CRUD operations
- Test permissions
- Test edge cases
- Test error handling
```

---

## 📋 PHASE 2: CORE FEATURES (WEEKS 3-5)

### WEEK 3: AI Interview System

#### Prompt 2.1: AI Interviewer Service

```
Build a sophisticated AI interviewer that conducts empathetic conversations:

1. app/services/ai/interviewer.py:

Create AIInterviewer class with:

Initialization:
- Load elder context (name, age, previous memories, preferences)
- Load question bank filtered by elder's background
- Initialize conversation state machine
- Set up GPT-4 system prompt

Core Methods:
- start_session(elder_id) -> InterviewSession
  - Create session record
  - Generate opening question based on elder's history
  - Consider: time of day, recent memories, suggested topics
  
- generate_next_question(previous_response: str, context: dict) -> Question
  - Analyze response for: completeness, emotion, energy level
  - Extract: people mentioned, places, dates, themes
  - Decide: follow-up question OR new topic
  - Use conversation tree algorithm
  - Return question with confidence score
  
- detect_emotion(text: str, audio_features: dict) -> EmotionAnalysis
  - Text sentiment analysis
  - Audio prosody analysis (if available)
  - Return: primary emotion, intensity, fatigue indicators
  
- should_continue(session_duration: int, emotion_history: list) -> Decision
  - Check session duration (don't exceed 30 min initially)
  - Check for fatigue signals
  - Check for distress signals
  - Recommend: continue, take break, end session, change topic
  
- adapt_difficulty(response_quality: float) -> None
  - If elder struggles, ask simpler questions
  - If elder is engaged, go deeper
  - Adjust based on cognitive indicators

Advanced Features:
- Multi-turn conversation tracking
- Context window management (keep last 10 exchanges)
- Personality consistency (maintain warm, patient tone)
- Cultural sensitivity (adapt to elder's background)
- Memory prevention (don't ask what's already recorded)

2. app/services/ai/question_bank.py:

Create QuestionBank class:
- Load 100+ pre-written questions from database
- Categorize by: era, topic, difficulty, sensitivity
- Tag questions with: follow_up_potential, emotional_intensity
- Provide method: get_appropriate_questions(elder_profile, session_context)

Question categories:
- Early Life (childhood, family, home, school, friends)
- Coming of Age (teenage years, first love, identity)
- Education & Career (learning, work, achievements, challenges)
- Love & Relationships (meeting spouse, marriage, parenthood)
- Historical Events (wars, cultural moments, societal changes)
- Hobbies & Passions (interests, talents, creative pursuits)
- Wisdom & Reflection (life lessons, regrets, advice, legacy)
- Spiritual & Philosophical (beliefs, values, purpose)

3. System prompt engineering:

Create dynamic prompt template:
```
You are a compassionate AI interviewer helping preserve {elder_name}'s life story.

CONTEXT:
- Elder: {name}, age {age}, from {hometown}
- Current conversation topic: {current_topic}
- Previous topics covered: {previous_topics}
- Energy level: {energy_assessment}
- Time in session: {session_duration}

YOUR ROLE:
- Ask warm, open-ended questions that invite storytelling
- Listen actively and ask relevant follow-ups
- Help them remember details through sensory prompts
- Be patient with pauses and confusion
- Recognize when they're tired and suggest breaks
- Celebrate their stories and validate experiences

GUIDELINES:
- One question at a time
- Start broad, then go specific
- Ask about sensory details (sights, sounds, smells)
- Reference their previous stories when relevant
- If they seem stuck, offer gentle prompts
- If emotional, acknowledge and give space
- Never rush or interrupt

CURRENT GOAL: {current_goal}

Generate the next question.
```

4. Conversation state machine:

States:
- OPENING: Warm greeting, set expectations
- EXPLORING: Ask primary questions
- DEEP_DIVE: Follow-up on interesting points
- WINDING_DOWN: Lighter topics, positive memories
- CLOSING: Thank them, preview next session

Transitions:
- Use finite state machine pattern
- Track state in session metadata
- Allow manual state override

5. Testing & Evaluation:

Create tests/test_interviewer.py:
- Test question generation variety
- Test emotional intelligence (mock responses)
- Test conversation coherence
- Test fatigue detection
- Test cultural sensitivity
- Measure conversation quality metrics

6. Configuration:

app/config/ai_config.py:
- GPT-4 model selection (gpt-4-turbo-preview recommended)
- Temperature settings (0.7 for balanced creativity)
- Max tokens per response
- Timeout settings
- Retry logic for API failures
- Cost tracking per session
```

#### Prompt 2.2: Audio Processing Pipeline

```
Build a complete audio processing system:

1. app/services/audio/transcription.py:

TranscriptionService class:

transcribe_audio(audio_file_path: str, language: str = "en") -> TranscriptionResult:
- Use OpenAI Whisper API
- Handle large files (chunk if > 25MB)
- Return: {
    text: str,
    segments: list[{start, end, text, confidence}],
    language: str,
    detected_language_confidence: float,
    duration: float,
    word_count: int,
    processing_time: float
  }

improve_transcription(raw_text: str, context: dict) -> str:
- Fix common transcription errors
- Add proper punctuation
- Capitalize proper nouns (use NLP)
- Fix homophones using context
- Format numbers, dates, times
- Add paragraph breaks at natural pauses

transcribe_streaming(audio_stream) -> AsyncGenerator:
- Real-time transcription for live interviews
- Yield partial results as they come
- Buffer for better accuracy
- Handle connection interruptions

2. app/services/audio/processing.py:

AudioProcessor class:

normalize_audio(audio_file) -> ProcessedAudio:
- Normalize volume levels
- Remove background noise (use noise reduction)
- Apply audio compression
- Convert to standard format (MP3 or WAV)
- Generate waveform data for visualization
- Extract audio features (pace, pitch, energy)

split_into_segments(audio_file, transcript) -> list[AudioSegment]:
- Split long recordings into memory chunks
- Use natural breaks in speech
- Each segment: 2-5 minutes ideal
- Align with transcript segments

generate_audio_fingerprint(audio_file) -> str:
- Create unique identifier for deduplication
- Use audio hashing algorithm

extract_features(audio_file) -> AudioFeatures:
- Pace (words per minute)
- Pitch variation (emotional indicators)
- Pause patterns (thoughtfulness, fatigue)
- Energy level (engagement)
- Background noise level
- Audio quality score

3. app/services/audio/storage.py:

AudioStorageService class:

upload_to_ipfs(audio_file, metadata: dict) -> IPFSResult:
- Upload to Pinata
- Set metadata (elder_id, memory_title, date, etc.)
- Get back CID and gateway URL
- Store mapping in database
- Set up pinning policy (keep forever)
- Return: {cid, gateway_url, file_size, ipfs_hash}

upload_private(audio_file, metadata: dict) -> PrivateFileResult:
- Use Pinata Files API for sensitive memories
- Generate secure access tokens
- Return: {file_id, access_url, expires_at}

get_audio_url(cid: str, access_level: str) -> str:
- Generate time-limited signed URL
- Check permissions
- Return CDN-optimized URL

backup_to_s3(audio_file, cid: str) -> None:
- Optional backup to traditional cloud storage
- For disaster recovery
- Keep CID as filename for verification

4. Background job system:

Use Celery or ARQ for async processing:

tasks/audio_tasks.py:
- process_audio_upload(memory_id, audio_file_path)
  - Transcribe → Process → Upload IPFS → Update DB
  - Send notifications on completion
  - Handle errors and retries

- batch_enrich_memories(elder_id)
  - Process all memories for historical context
  - Run during off-peak hours

5. File handling:

app/utils/file_utils.py:
- Secure file upload handling
- Temporary file cleanup
- File type validation
- Virus scanning (ClamAV integration)
- Max file size enforcement

6. Testing:

tests/test_audio_processing.py:
- Test transcription accuracy with sample audio
- Test audio normalization
- Test IPFS upload/retrieval
- Test error handling (corrupted files, network issues)
- Performance benchmarks

7. Configuration:

config/audio_config.py:
- Supported formats: mp3, wav, m4a, ogg
- Max file size: 500MB
- Quality settings for compression
- Whisper model selection (large-v3 for best accuracy)
- Pinata API configuration
- Temporary storage location
```

#### Prompt 2.3: Memory Enrichment AI

```
Implement AI-powered memory enrichment system:

1. app/services/ai/enrichment.py:

MemoryEnricher class:

enrich_memory(memory: Memory) -> EnrichedMemory:
- Run multiple enrichment processes in parallel
- Combine results
- Update memory in database
- Return enriched memory

extract_entities(transcription: str) -> EntityExtraction:
- Use spaCy or GPT-4 to extract:
  - People (names, relationships)
  - Places (cities, buildings, landmarks)
  - Dates (specific dates, time periods, ages)
  - Events (historical events, personal milestones)
  - Organizations (companies, schools, military units)
- Return structured data with confidence scores

add_historical_context(memory: Memory) -> HistoricalContext:
- Analyze time period mentioned
- Fetch relevant historical events from knowledge base
- Generate context paragraph:
  "In 1955 when John was stationed in Korea, the Korean War had 
   recently ended. The country was rebuilding, and U.S. troops 
   provided security and aid. This was also the year..."
- Include: major events, cultural trends, economic conditions
- Cite sources for fact-checking

categorize_memory(transcription: str, existing_categories: list) -> Classification:
- Primary category (childhood, career, family, etc.)
- Secondary categories (military, education, hobbies)
- Era/decade (1940s, 1950s, etc.)
- Themes (adversity, love, loss, triumph, humor)
- Content warnings (war, death, trauma) if needed

analyze_emotion(transcription: str, audio_features: dict) -> EmotionalAnalysis:
- Primary emotion (joyful, nostalgic, sad, proud, reflective)
- Intensity (1-10 scale)
- Emotional arc (how emotion changes through story)
- Trigger warnings if needed
- Combine text sentiment + audio prosody

identify_connections(memory: Memory, all_memories: list[Memory]) -> Connections:
- Find related memories by:
  - Shared people
  - Same location
  - Similar time period
  - Same theme
- Calculate similarity scores
- Return top 5 related memories

generate_summary(transcription: str) -> Summary:
- One-sentence summary for cards
- 2-3 sentence preview
- Key points list
- Auto-generate title if missing

extract_wisdom(transcription: str) -> Wisdom:
- Identify life lessons
- Extract advice
- Find philosophical insights
- Categorize wisdom (parenting, career, relationships)

2. app/services/ai/knowledge_base.py:

HistoricalKnowledgeBase class:
- Load historical events database (JSON or DB)
- Methods:
  - get_events_by_year(year: int) -> list[Event]
  - get_context_for_period(start_year, end_year) -> str
  - search_events(keywords: list) -> list[Event]
- Data sources:
  - Wikipedia API
  - Historical databases
  - Pre-compiled events JSON

3. Batch processing:

tasks/enrichment_tasks.py:
- enrich_memory_task(memory_id: int)
  - Async task for background enrichment
  - Update progress in database
  - Notify on completion

- batch_enrich_elder_memories(elder_id: int)
  - Enrich all un-enriched memories
  - Process in batches of 10
  - Rate limit API calls

4. Quality assurance:

app/services/ai/qa.py:
- Verify enrichment quality
- Flag low-confidence extractions for manual review
- Detect hallucinations (compare entities to transcription)
- Calculate enrichment completeness score

5. Caching:

- Cache historical context by decade (rarely changes)
- Cache common entity extractions
- Use Redis for fast access

6. Testing:

tests/test_enrichment.py:
- Test entity extraction accuracy
- Test historical context relevance
- Test categorization consistency
- Test with edge cases (short memories, unclear audio)

7. Configuration:

config/enrichment_config.py:
- Enable/disable specific enrichments
- Configure AI model settings
- Set confidence thresholds
- Define batch sizes and rate limits
```

### WEEK 4-5: Frontend Dashboard

#### Prompt 2.4: Dashboard UI Foundation

```
Build a beautiful, functional family dashboard:

1. src/app/dashboard/layout.tsx:

Dashboard layout with:
- Sidebar navigation:
  - Home (overview)
  - Memories (library)
  - Timeline (visualization)
  - Family (members)
  - Settings
- Top bar:
  - Elder selector dropdown (if multiple elders)
  - Search bar (global search)
  - Notifications bell
  - User menu
- Responsive: sidebar collapses on mobile, becomes bottom nav

Styling:
- Use shadcn/ui components
- Warm, nostalgic color palette
- Vintage photo aesthetic
- High contrast for accessibility
- Large text (16px minimum)

2. src/app/dashboard/page.tsx:

Dashboard home with widgets:

Stats Cards:
- Total Memories (with trend from last month)
- Hours Recorded (total duration)
- Timeline Completeness (% of decades covered)
- Family Members (active count)

Recent Memories:
- Grid of 6 most recent memory cards
- Audio player preview
- Quick actions (play, share, edit)

Activity Feed:
- Recent family activity
- New memories added
- Comments or reactions
- Upcoming birthdays (to prompt new recordings)

Quick Actions:
- Start Interview (prominent CTA)
- Add Memory Manually
- Invite Family Member
- Export Memories

Memory