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

Memory Collections Widget:
- Themed collections
- Auto-generated based on AI

---

## 📋 PREMIUM FEATURES IMPLEMENTATION (PHASE 5: WEEKS 13-16)

### WEEK 13: Subscription & Pricing Infrastructure

#### Prompt 5.1: Subscription System Architecture

```
Design and implement a comprehensive subscription and pricing system:

1. Database Schema - Create new models:

app/db/models/subscription.py:
- Subscription model:
  - user_id (FK to users)
  - plan_tier (enum: free, premium, enterprise)
  - status (enum: active, cancelled, past_due, trialing)
  - billing_cycle (enum: monthly, annual)
  - current_period_start, current_period_end
  - stripe_subscription_id, stripe_customer_id
  - price_id, amount_cents, currency
  - trial_ends_at
  - cancelled_at, cancel_at_period_end
  - metadata JSONB (discount info, promo codes)
  - created_at, updated_at

- SubscriptionPlan model:
  - name (Free, Premium, Enterprise)
  - tier_level (0, 1, 2)
  - price_monthly, price_annual
  - stripe_price_id_monthly, stripe_price_id_annual
  - features JSONB
  - limits JSONB (voice_clones, memories, storage_gb, etc.)
  - is_active, is_visible
  - sort_order

- UsageTracking model:
  - user_id, subscription_id
  - period_start, period_end
  - voice_clones_created, voice_clones_limit
  - tts_characters_used, tts_characters_limit
  - memories_created, memories_limit
  - storage_bytes_used, storage_bytes_limit
  - api_calls_count
  - premium_features_used JSONB
  - updated_at

- PaymentHistory model:
  - user_id, subscription_id
  - stripe_payment_intent_id
  - amount_cents, currency
  - status (succeeded, failed, pending)
  - payment_method_type
  - invoice_url, receipt_url
  - created_at

2. Feature Tier Configuration:

app/core/plans.py:

PLAN_FEATURES = {
    "free": {
        "name": "Free",
        "price_monthly": 0,
        "voice_clones_limit": 1,
        "memories_limit": 50,
        "storage_gb": 1,
        "tts_characters_per_month": 10000,
        "tts_max_chars_per_request": 500,
        "audio_quality": "standard",  # mp3_44100_64
        "models": ["eleven_multilingual_v2"],
        "voice_emotions": False,
        "voice_mixing": False,
        "batch_processing": False,
        "background_music": False,
        "multi_voice_narration": False,
        "memory_enhancement": False,
        "export_formats": ["mp3"],
        "api_access": False,
        "priority_support": False,
        "analytics_dashboard": "basic",
        "family_members_limit": 5,
        "collaboration_features": False,
    },
    "premium": {
        "name": "Premium",
        "price_monthly": 29.99,
        "price_annual": 299.99,  # 2 months free
        "voice_clones_limit": 10,
        "memories_limit": 1000,
        "storage_gb": 50,
        "tts_characters_per_month": 500000,
        "tts_max_chars_per_request": 5000,
        "audio_quality": "high",  # mp3_44100_192
        "models": ["eleven_multilingual_v2", "eleven_turbo_v2"],
        "voice_emotions": True,
        "voice_styles": ["conversational", "narrative", "emotional"],
        "voice_mixing": True,
        "batch_processing": True,
        "background_music": True,
        "multi_voice_narration": True,
        "memory_enhancement": True,  # AI improves stories
        "ssml_support": True,
        "custom_pronunciations": True,
        "export_formats": ["mp3", "wav", "m4a"],
        "api_access": "basic",
        "priority_support": True,
        "analytics_dashboard": "advanced",
        "family_members_limit": 25,
        "collaboration_features": True,
        "memory_compilations": True,
        "emotion_detection": True,
    },
    "enterprise": {
        "name": "Enterprise",
        "price_monthly": 99.99,
        "price_annual": 999.99,
        "voice_clones_limit": -1,  # unlimited
        "memories_limit": -1,
        "storage_gb": 500,
        "tts_characters_per_month": 2000000,
        "tts_max_chars_per_request": 10000,
        "audio_quality": "premium",  # pcm_44100
        "models": ["all"],
        "voice_emotions": True,
        "voice_styles": "all",
        "voice_mixing": True,
        "voice_versioning": True,
        "batch_processing": True,
        "background_music": True,
        "multi_voice_narration": True,
        "memory_enhancement": True,
        "ssml_support": True,
        "custom_pronunciations": True,
        "white_label": True,
        "export_formats": ["all"],
        "api_access": "full",
        "api_rate_limit": 1000,  # per minute
        "priority_processing": True,
        "dedicated_support": True,
        "analytics_dashboard": "enterprise",
        "family_members_limit": -1,
        "collaboration_features": True,
        "memory_compilations": True,
        "emotion_detection": True,
        "custom_models": True,
        "sso": True,
        "audit_logs": True,
    }
}

3. Alembic Migration:

alembic/versions/xxx_add_subscription_system.py:
- Create subscription tables
- Add indexes on user_id, status, stripe_subscription_id
- Seed default plans
- Migrate existing users to free tier
```

#### Prompt 5.2: Stripe Payment Integration

```
Implement Stripe payment processing:

1. app/services/payment/stripe_service.py:

StripeService class:

create_customer(user: User) -> stripe.Customer:
- Create Stripe customer
- Store stripe_customer_id in user record
- Set metadata (user_id, email)
- Add default payment method if provided

create_subscription(
    user_id: int,
    plan_tier: str,
    billing_cycle: str,
    payment_method_id: str = None
) -> Subscription:
- Get plan details
- Create Stripe subscription
- Store in database
- Start trial if applicable (14 days free)
- Send confirmation email
- Return subscription object

update_subscription(
    subscription_id: int,
    new_plan_tier: str = None,
    billing_cycle: str = None
) -> Subscription:
- Prorate charges
- Update Stripe subscription
- Update database
- Send notification

cancel_subscription(
    subscription_id: int,
    cancel_immediately: bool = False
) -> Subscription:
- Cancel at period end OR immediately
- Update Stripe
- Update database status
- Schedule data retention (30 days grace period)

reactivate_subscription(subscription_id: int) -> Subscription:
- Resume cancelled subscription
- Update Stripe
- Update database

handle_payment_success(stripe_event: dict) -> None:
- Update subscription status
- Record payment in PaymentHistory
- Reset usage counters for new period
- Send receipt email

handle_payment_failed(stripe_event: dict) -> None:
- Update subscription to past_due
- Notify user
- Retry payment (Stripe handles this)
- Downgrade if payment fails 3 times

handle_subscription_updated(stripe_event: dict) -> None:
- Sync Stripe changes to database
- Handle plan changes, cancellations

2. Webhook Endpoint:

app/api/v1/endpoints/webhooks.py:

POST /webhooks/stripe:
- Verify webhook signature
- Handle events:
  - customer.subscription.created
  - customer.subscription.updated
  - customer.subscription.deleted
  - invoice.payment_succeeded
  - invoice.payment_failed
  - payment_intent.succeeded
  - payment_intent.payment_failed
- Process asynchronously
- Return 200 immediately

3. Frontend Integration:

packages/frontend/src/lib/stripe.ts:
- Initialize Stripe.js
- Payment element component
- Checkout flow

packages/frontend/src/app/settings/billing/page.tsx:
- Current plan display
- Usage metrics
- Upgrade/downgrade options
- Payment method management
- Billing history
- Invoice downloads

packages/frontend/src/components/pricing/PricingCards.tsx:
- Pricing table
- Feature comparison
- CTA buttons
- Annual/monthly toggle

4. Security:

app/core/stripe_config.py:
- Webhook signature verification
- API key management
- Idempotency keys for requests
- Retry logic with exponential backoff

5. Testing:

tests/test_stripe.py:
- Mock Stripe API calls
- Test subscription lifecycle
- Test webhook processing
- Test edge cases (expired cards, etc.)
```

#### Prompt 5.3: Usage Tracking & Enforcement

```
Implement usage tracking and limit enforcement:

1. app/services/usage/usage_tracker.py:

UsageTracker class:

track_voice_clone_creation(user_id: int, voice_id: str) -> None:
- Increment voice_clones_created
- Check against limit
- Raise error if exceeded
- Update database

track_tts_usage(user_id: int, character_count: int) -> None:
- Add to tts_characters_used
- Check monthly limit
- Raise error if exceeded
- Log usage for analytics

track_memory_creation(user_id: int, memory_id: int) -> None:
- Increment memories_created
- Check limit
- Track storage usage

track_storage(user_id: int, file_size_bytes: int) -> None:
- Add to storage_bytes_used
- Check storage limit
- Suggest upgrade if near limit

get_usage_summary(user_id: int) -> UsageSummary:
- Current period usage
- Limits for plan
- Percentage used
- Projected usage for month
- Recommendations

reset_monthly_usage(user_id: int) -> None:
- Called at billing cycle renewal
- Reset character counts
- Keep historical data

2. Middleware for enforcement:

app/api/middleware/subscription_middleware.py:

check_feature_access(feature: str):
- Decorator for endpoints
- Verify user has access to feature
- Return 402 Payment Required if not
- Include upgrade URL in response

check_usage_limit(resource_type: str):
- Check before resource creation
- Soft limit (warn at 80%)
- Hard limit (block at 100%)
- Suggest upgrade

Example usage:
@app.post("/voices/clone")
@check_feature_access("voice_cloning")
@check_usage_limit("voice_clones")
async def clone_voice(...):
    ...

3. app/services/usage/analytics.py:

UsageAnalytics class:

generate_usage_report(user_id: int, period: str) -> Report:
- Detailed usage breakdown
- Cost analysis
- Feature utilization
- Recommendations for plan optimization

predict_usage_trend(user_id: int) -> Prediction:
- Analyze historical usage
- Predict next month usage
- Suggest plan if needed

identify_power_users() -> list[User]:
- Find users hitting limits
- Target for upsell
- Offer custom plans

4. Database queries:

app/db/repositories/usage_repository.py:
- Efficient usage queries
- Aggregations for analytics
- Caching for frequently accessed data

5. Notifications:

app/services/notifications/usage_notifications.py:
- Notify at 50%, 80%, 90%, 100% of limit
- Upgrade suggestions
- Feature discovery (unused premium features)
```

### WEEK 14: Premium Voice Features

#### Prompt 5.4: Enhanced Voice Capabilities

```
Implement premium voice features:

1. app/services/elevenlabs/premium_voice_service.py:

PremiumVoiceService class (extends ElevenLabsService):

clone_with_emotions(
    audio_files: list,
    emotion_samples: dict[str, list]
) -> EmotionalVoice:
- Accept samples for different emotions
- Happy samples, sad samples, angry samples
- Create multi-emotional voice profile
- Store emotion mappings
- Return voice_id with emotion capabilities

text_to_speech_with_emotion(
    text: str,
    voice_id: str,
    emotion: str = "neutral",
    intensity: float = 0.5
) -> bytes:
- Apply emotion to TTS
- Adjust voice settings for emotion:
  - Happy: higher stability, more variation
  - Sad: lower energy, slower pace
  - Angry: more intensity, sharper tone
- Use style parameter in ElevenLabs API

blend_voices(
    voice_ids: list[str],
    weights: list[float],
    text: str
) -> bytes:
- Mix multiple voices (Premium feature)
- Weighted average of voice characteristics
- Create unique hybrid voices
- Use for different narrators in same memory

create_voice_variations(
    base_voice_id: str,
    variations: list[str]
) -> list[VoiceVariation]:
- Create aged versions (younger/older)
- Create emotional variations
- Store as separate voice profiles
- Link to base voice for management

apply_ssml(text: str, voice_id: str) -> bytes:
- Parse SSML markup (Premium feature)
- Support for:
  - <prosody rate="slow"> (speed control)
  - <emphasis> (stress words)
  - <break time="1s"> (pauses)
  - <say-as> (numbers, dates)
- Enhanced control for premium users

batch_text_to_speech(
    texts: list[str],
    voice_id: str,
    options: dict
) -> list[bytes]:
- Process multiple texts in parallel
- Queue management
- Progress tracking
- Combine into single audio file if requested

2. app/services/audio/enhancement_service.py:

AudioEnhancementService class:

enhance_memory_story(
    transcription: str,
    elder_context: dict
) -> EnhancedStory:
- Use GPT-4 to improve storytelling (Premium)
- Add sensory details
- Improve flow and pacing
- Maintain authenticity
- Flag changes for review
- Return: original, enhanced, diff

add_background_music(
    audio_bytes: bytes,
    mood: str,
    intensity: float = 0.3
) -> bytes:
- Select appropriate music (library or AI-generated)
- Mix with voice audio
- Adjust volume (music should be subtle)
- Fade in/out at boundaries
- Moods: nostalgic, joyful, reflective, melancholic

create_multi_voice_narration(
    memory: Memory,
    voice_mappings: dict[str, str]
) -> bytes:
- Parse memory for different speakers
- Identify quoted speech
- Apply different voices to different parts
- Narrator vs quoted person
- Smooth transitions between voices

detect_and_adjust_emotion(
    text: str,
    audio_features: dict
) -> EmotionAdjustment:
- Analyze emotional content (Premium AI)
- Suggest TTS settings for each segment
- Auto-adjust voice parameters
- Create emotional arc in narration

3. app/services/audio/compilation_service.py:

CompilationService class (Premium):

create_memory_compilation(
    memory_ids: list[int],
    options: CompilationOptions
) -> Compilation:
- Combine multiple memories into audiobook
- Add chapter markers
- Include intro/outro
- Background music between chapters
- Export as single MP3 or by chapter
- Generate metadata (title, description)
- Options:
  - include_summaries (AI-generated intros)
  - background_music (bool)
  - voice_consistency (use same voice clone)
  - chapter_separation (silence duration)

create_themed_compilation(
    elder_id: int,
    theme: str
) -> Compilation:
- Auto-select memories by theme
- "Career Journey", "Love Story", "War Years"
- Order chronologically
- Create narrative flow
- Generate title and description

4. Voice Library Management:

app/api/v1/endpoints/premium/voices.py:

GET /premium/voices/{voice_id}/emotions:
- List available emotions for voice
- Return sample audio for each

POST /premium/voices/{voice_id}/variations:
- Create voice variation
- Specify: aged_by_years, emotion_base, style

POST /premium/voices/blend:
- Blend multiple voices
- Preview before saving

GET /premium/voices/{voice_id}/usage-analytics:
- Track which voices used most
- Quality metrics
- User preferences

5. Testing:

tests/test_premium_voice.py:
- Test emotion application
- Test voice blending
- Test SSML parsing
- Test audio enhancement quality
```

#### Prompt 5.5: Memory Enhancement AI (Premium)

```
Build advanced AI features for memory enhancement:

1. app/services/ai/premium/memory_enhancer.py:

MemoryEnhancer class (Premium):

enhance_storytelling(transcription: str, context: dict) -> Enhancement:
- Analyze story structure
- Identify missing details
- Add sensory descriptions:
  "The old barn" → "The weathered red barn with its fading paint"
- Improve pacing (fix run-on sentences)
- Enhance dialogue
- Preserve authenticity (mark all additions)
- Return: {
    enhanced_text: str,
    changes: list[Change],
    confidence_score: float,
    review_required: bool
  }

generate_story_variations(memory: Memory) -> list[Variation]:
- Short version (30-second summary)
- Medium version (2-minute highlights)
- Full version (complete story)
- Child-friendly version (simplified language)
- Each variation maintains key details

detect_emotion_arc(transcription: str) -> EmotionArc:
- Track emotional progression through story
- Identify: beginning emotion, climax, resolution
- Suggest voice modulation points
- Return arc data for visualization
- Use for emotion-aware TTS

extract_quotable_moments(memory: Memory) -> list[Quote]:
- Find meaningful phrases
- Life lessons, wisdom, humor
- Format for social sharing
- Generate quote cards (with context)

identify_story_gaps(elder_memories: list[Memory]) -> GapAnalysis:
- Analyze collection for missing periods
- Suggest interview topics to fill gaps
- "You have no memories from 1965-1970"
- Generate targeted questions

suggest_memory_connections(memory: Memory) -> Suggestions:
- Find thematic connections
- Suggest creating compilations
- Recommend next memory to record
- Build narrative arcs across memories

2. app/services/ai/premium/advanced_enrichment.py:

AdvancedEnrichment class (Premium):

generate_multimedia_enhancement(memory: Memory) -> Enhancement:
- Suggest relevant images (historical photos)
- Find archival footage (if available)
- Locate maps of mentioned places
- Find historical documents
- Return resource URLs and descriptions

create_memory_timeline_entry(memory: Memory) -> TimelineEntry:
- Extract precise dates/periods
- Create visual timeline entry
- Add context bubbles
- Link related events
- Include historical markers

analyze_historical_accuracy(memory: Memory) -> AccuracyReport:
- Cross-reference with historical records
- Flag potential date inconsistencies
- Suggest corrections (with confidence)
- Cite sources
- Generate fact-check report

enrich_with_cultural_context(memory: Memory) -> CulturalContext:
- Identify cultural references
- Explain traditions mentioned
- Add context for younger generations
- Translate idioms/slang from that era
- Include social/political context

3. Background Processing:

tasks/premium_enhancement_tasks.py:

enhance_memory_premium(memory_id: int):
- Run all premium enhancements
- Process in background (don't block)
- Update progress in real-time
- Notify on completion
- Allow manual review before applying

batch_enhance_collection(elder_id: int):
- Enhance all memories
- Prioritize by importance/plays
- Rate limit API usage
- Generate collection insights

4. Quality Control:

app/services/ai/premium/qa_service.py:

review_enhancement_quality(original: str, enhanced: str) -> QAResult:
- Check authenticity preservation
- Verify factual consistency
- Measure improvement metrics
- Flag hallucinations
- Require human review if quality low

5. User Interface:

packages/frontend/src/components/premium/MemoryEnhancer.tsx:
- Side-by-side comparison (original vs enhanced)
- Highlight changes (color-coded)
- Accept/reject individual changes
- Bulk accept/reject
- Provide feedback to improve AI

6. Analytics:

track_enhancement_usage(user_id: int, enhancement_type: str):
- Which features are most used
- User satisfaction with enhancements
- Acceptance rate of AI suggestions
- Time saved vs manual editing
```

### WEEK 15: Advanced Analytics & Collaboration

#### Prompt 5.6: Premium Analytics Dashboard

```
Build comprehensive analytics for premium users:

1. app/services/analytics/premium_analytics.py:

PremiumAnalytics class:

generate_collection_insights(elder_id: int) -> CollectionInsights:
- Total memories: count, hours, words
- Coverage analysis:
  - Timeline completeness (% of life covered)
  - Decade breakdown
  - Category distribution
- Engagement metrics:
  - Most played memories
  - Family engagement score
  - Comments/reactions count
- Quality metrics:
  - Audio quality average
  - Transcription accuracy
  - Enrichment completeness
- Growth trends:
  - Memories per month
  - Recording frequency
  - Family activity

analyze_themes_and_patterns(elder_id: int) -> ThemeAnalysis:
- Dominant themes (career, family, hobbies)
- Recurring people/places
- Emotional patterns over time
- Life milestones coverage
- Character arc (personality evolution)
- Generate narrative summary

predict_content_opportunities(elder_id: int) -> Opportunities:
- Topics that need more coverage
- Suggested interview questions
- Best time to interview (based on patterns)
- Compilation ideas
- Trending memories (family interest)

generate_family_engagement_report(elder_id: int) -> EngagementReport:
- Who's listening most
- Favorite memories by person
- Comment analysis
- Suggested content for each family member
- Engagement trends over time

calculate_collection_value(elder_id: int) -> ValueMetrics:
- Estimated hours to recreate
- Historical value (unique stories)
- Educational value
- Emotional impact score
- Legacy preservation score

2. Data Visualization:

app/api/v1/endpoints/premium/analytics.py:

GET /premium/analytics/timeline:
- Return data for timeline visualization
- Memories plotted on life timeline
- Historical events overlay
- Gaps and density visualization

GET /premium/analytics/network:
- People network graph
- Connections between individuals
- Frequency of mentions
- Relationship strength

GET /premium/analytics/emotion-journey:
- Emotional arc across life
- Sentiment analysis over time
- Key emotional moments
- Mood patterns

GET /premium/analytics/themes:
- Theme distribution (pie/bar chart)
- Theme evolution over time
- Cross-theme connections

GET /premium/analytics/engagement:
- Family engagement over time
- Individual listening patterns
- Peak engagement times
- Content preferences

3. Custom Reports:

app/services/analytics/report_generator.py:

generate_pdf_report(elder_id: int, report_type: str) -> PDF:
- Professional PDF report
- Include visualizations
- Key insights and statistics
- Recommendations
- Export option for sharing
- Report types:
  - Monthly summary
  - Annual review
  - Collection overview
  - Family engagement report

generate_presentation(elder_id: int) -> PPTX:
- Create slideshow of memories
- Include stats and highlights
- For family gatherings
- Export as PowerPoint/PDF

4. Real-time Analytics:

app/services/analytics/realtime.py:

setup_analytics_stream(user_id: int) -> WebSocket:
- Real-time usage updates
- Live family activity feed
- Processing status updates
- Notification stream

5. Comparative Analytics (Enterprise):

app/services/analytics/benchmarking.py:

get_industry_benchmarks() -> Benchmarks:
- Compare to average users
- Percentile rankings
- Best practices suggestions
- Optimization opportunities

6. Export & Sharing:

POST /premium/analytics/export:
- Export raw data (CSV, JSON)
- Custom date ranges
- Filtered by category/theme
- Include metadata
- Schedule regular exports

7. Frontend Dashboard:

packages/frontend/src/app/premium/analytics/page.tsx:
- Interactive charts (Chart.js/Recharts)
- Filters and date ranges
- Export buttons
- Drill-down capabilities
- Mobile-responsive

packages/frontend/src/components/premium/charts/:
- TimelineChart.tsx
- ThemeDistribution.tsx
- EngagementHeatmap.tsx
- EmotionJourney.tsx
- FamilyNetwork.tsx
```

#### Prompt 5.7: Collaboration Features (Premium)

```
Implement family collaboration features:

1. app/services/collaboration/family_collaboration.py:

FamilyCollaboration class:

invite_family_member(
    inviter_id: int,
    email: str,
    role: str,
    permissions: dict
) -> Invitation:
- Generate secure invitation link
- Set expiration (7 days)
- Define access level (viewer, contributor, editor)
- Send email invitation
- Track invitation status

manage_permissions(
    elder_id: int,
    family_member_id: int,
    permissions: dict
) -> Permissions:
- Granular permissions:
  - can_view_all_memories (bool)
  - can_view_private_memories (bool)
  - can_create_memories (bool)
  - can_edit_memories (bool)
  - can_delete_memories (bool)
  - can_invite_members (bool)
  - can_export_data (bool)
  - can_manage_billing (bool)
- Role presets (Viewer, Contributor, Admin)
- Custom role builder (Premium)

2. Collaborative Memory Creation:

app/api/v1/endpoints/collaboration/memories.py:

POST /collaboration/memories/{memory_id}/comments:
- Add comment to memory
- Support threads
- Mention family members (@name)
- Attach media to comments

POST /collaboration/memories/{memory_id}/reactions:
- React with emoji
- Track who reacted
- Show reaction counts

POST /collaboration/memories/{memory_id}/corrections:
- Suggest corrections to transcription
- Track who suggested
- Approve/reject workflow
- Show version history

POST /collaboration/memories/{memory_id}/tags:
- Collaborative tagging
- Tag suggestions
- Tag voting (most used tags highlighted)

3. Shared Memory Collections:

app/services/collaboration/shared_collections.py:

create_shared_collection(
    creator_id: int,
    name: str,
    memory_ids: list[int],
    share_settings: dict
) -> SharedCollection:
- Create curated collection
- Set privacy (private, family-only, public)
- Generate shareable link
- Track views and engagement

share_collection_externally(
    collection_id: int,
    expiration: datetime = None
) -> ShareLink:
- Generate public link
- Optional password protection
- Expiration date
- Track external views
- Embeddable player

4. Activity Feed & Notifications:

app/services/collaboration/activity_feed.py:

get_family_activity(
    elder_id: int,
    limit: int = 20
) -> ActivityFeed:
- Recent family actions:
  - New memories added
  - Comments posted
  - Tags added
  - Reactions given
  - Corrections suggested
  - Collections created
- Real-time updates (WebSocket)
- Filter by member or type

notify_family(
    elder_id: int,
    event_type: str,
    data: dict
) -> None:
- Send notifications based on preferences:
  - Email (daily digest, immediate)
  - Push notifications
  - In-app notifications
- Notification types:
  - New memory added
  - Comment on your memory
  - Mention in comment
  - Memory milestone (100th memory!)
  - Elder birthday reminder

5. Collaborative Interview Sessions:

app/services/collaboration/group_interview.py:

create_group_session(
    elder_id: int,
    participant_ids: list[int]
) -> GroupSession:
- Multiple family members join interview
- Take turns asking questions
- Shared question queue
- Live transcription for all
- Post-session: everyone can add notes

6. Family Workspace (Premium):

app/api/v1/endpoints/collaboration/workspace.py:

GET /collaboration/workspace/{elder_id}:
- Central hub for family collaboration
- Upcoming interviews scheduled
- Task assignments (who interviews next)
- Shared notes and research
- Family tree integration
- Calendar integration

POST /collaboration/workspace/tasks:
- Assign tasks:
  - "Interview grandpa about military service"
  - "Find photos from 1960s wedding"
  - "Verify dates in Korea story"
- Due dates and reminders
- Status tracking (todo, in-progress, done)

7. Version Control for Memories:

app/services/collaboration/versioning.py:

save_memory_version(
    memory_id: int,
    changes: dict,
    editor_id: int
) -> Version:
- Track all changes to memories
- Store diffs, not full copies
- Attribute changes to users
- Revert to previous versions
- Show change history

8. Frontend Components:

packages/frontend/src/components/collaboration/:
- CommentThread.tsx (nested comments)
- MemberPermissions.tsx (permission matrix)
- ActivityFeed.tsx (real-time updates)
- SharedCollectionPlayer.tsx (public player)
- CollaborativeEditor.tsx (multi-user editing)
- FamilyWorkspace.tsx (task management)

9. Access Control:

app/middleware/collaboration_middleware.py:
- Check permissions before all operations
- Row-level security for memories
- Audit log for sensitive actions
- Rate limiting per family member
```

### WEEK 16: API Access & Enterprise Features

#### Prompt 5.8: Public API & Developer Tools

```
Build public API for Premium/Enterprise users:

1. app/api/v1/endpoints/developer/api_keys.py:

APIKeyManagement:

POST /developer/api-keys:
- Generate API key
- Set scoped permissions:
  - read:memories
  - write:memories
  - read:elders
  - write:elders
  - voice:clone
  - voice:tts
- Set rate limits per key
- Optional expiration
- Return: {key_id, secret_key (show once)}

GET /developer/api-keys:
- List all keys
- Show usage stats per key
- Show last used timestamp
- Show permissions

DELETE /developer/api-keys/{key_id}:
- Revoke API key
- Audit log the revocation

GET /developer/api-keys/{key_id}/usage:
- Detailed usage analytics
- Requests per endpoint
- Error rates
- Rate limit hits
- Cost attribution

2. Public API Endpoints:

app/api/public/v1/memories.py:

GET /api/v1/memories:
- List memories (with API key auth)
- Pagination, filters, search
- Rate limited by plan

POST /api/v1/memories:
- Create memory via API
- Upload audio or provide transcription
- Webhook callback on completion

GET /api/v1/memories/{id}:
- Retrieve memory details
- Include audio URL (signed)

POST /api/v1/voices/clone:
- Voice cloning via API
- Upload samples
- Async processing
- Webhook on completion

POST /api/v1/text-to-speech:
- TTS via API
- Character counting
- Quality selection by plan
- Return audio URL

3. API Documentation:

app/api/public/v1/docs.py:
- OpenAPI 3.0 spec
- Interactive docs (Swagger UI)
- Code examples (Python, JS, cURL)
- Authentication guide
- Rate limit documentation
- Webhook setup guide

4. SDK Generation:

scripts/generate_sdks.py:
- Auto-generate client libraries:
  - Python SDK
  - JavaScript/TypeScript SDK
  - Go SDK
- Publish to package managers
- Include TypeScript types
- Include examples

5. Webhooks:

app/services/webhooks/webhook_service.py:

register_webhook(
    user_id: int,
    url: str,
    events: list[str],
    secret: str
) -> Webhook:
- Register webhook endpoint
- Events:
  - memory.created
  - memory.enriched
  - voice.cloned
  - session.completed
  - transcription.completed
- Generate webhook secret
- Verify SSL certificate

send_webhook(
    webhook_id: int,
    event: str,
    payload: dict
) -> None:
- Sign payload with secret
- Retry logic (3 attempts)
- Exponential backoff
- Log delivery status
- Alert on failures

6. Rate Limiting:

app/middleware/api_rate_limiter.py:
- Rate limits by plan:
  - Free: N/A (no API access)
  - Premium: 100 req/min
  - Enterprise: 1000 req/min
- Different limits per endpoint
- Return 429 with Retry-After header
- Track usage for billing

7. API Analytics:

app/services/developer/api_analytics.py:

generate_api_usage_report(user_id: int) -> APIReport:
- Requests per day/week/month
- Endpoints hit frequency
- Error rate by endpoint
- Latency percentiles
- Cost breakdown
- Optimization suggestions

8. Enterprise Features:

app/api/enterprise/custom_models.py:

POST /enterprise/models/train:
- Train custom voice model (Enterprise only)
- Upload training data
- Specify training parameters
- Monitor training progress
- Evaluate model quality

POST /enterprise/models/deploy:
- Deploy custom model
- A/B testing support
- Rollback capability

GET /enterprise/audit-logs:
- Complete audit trail
- All actions by all users
- Export for compliance
- GDPR-ready format

POST /enterprise/sso/configure:
- Single Sign-On setup
- SAML 2.0 support
- Azure AD, Okta, Google Workspace
- User provisioning (SCIM)

9. Developer Portal:

packages/frontend/src/app/developer/page.tsx:
- API key management UI
- Usage dashboard
- Documentation browser
- Code playground (test API calls)
- Webhook tester
- SDK downloads
- Community forum link

10. Example Integrations:

docs/examples/:
- Zapier integration guide
- Slack bot for memory notifications
- iOS shortcut for quick recording
- Home Assistant integration
- Obsidian plugin for personal notes
- Custom CRM integration
```

#### Prompt 5.9: Monetization & Growth Features

```
Implement features to drive upgrades and retention:

1. In-App Upgrade Prompts:

packages/frontend/src/components/monetization/UpgradePrompt.tsx:
- Smart upgrade prompts:
  - Show when hitting limits
  - Highlight specific premium features
  - "Unlock emotions for this voice"
  - "Upgrade to store unlimited memories"
- A/B tested messaging
- Dismissable but reminder cadence
- Track conversion rates

packages/frontend/src/components/monetization/FeatureUpsell.tsx:
- Contextual feature promotion:
  - Show "Enhance with AI" on free tier (locked)
  - Show "Create compilation" (locked)
  - Click shows value proposition + upgrade CTA
- Video demos of premium features
- Testimonials

2. Free Trial Management:

app/services/billing/trial_service.py:

start_trial(user_id: int, plan: str) -> Trial:
- 14-day free trial (Premium)
- Full feature access
- Auto-downgrade at end (no CC required)
- Email drip campaign during trial:
  - Day 1: Welcome, getting started
  - Day 3: Feature highlights
  - Day 7: Halfway reminder
  - Day 12: Last chance, testimonials
  - Day 14: Trial ending
  - Day 16: We miss you (win-back)

extend_trial(user_id: int, days: int) -> Trial:
- Manual trial extension (CS tool)
- Reward for feedback/testimonials
- Win-back strategy

3. Usage-Based Suggestions:

app/services/billing/smart_upgrade.py:

suggest_upgrade(user_id: int) -> Suggestion:
- Analyze usage patterns
- "You've hit your voice clone limit 3 times"
- "You could save $X with annual billing"
- "You're using 5 premium features regularly"
- Calculate ROI for user
- Personalized upgrade path

detect_at_risk_churners() -> list[User]:
- Low engagement (no login 14 days)
- Cancellation indicators
- Feature abandonment
- Send win-back campaigns

4. Referral Program (Premium users):

app/services/marketing/referral_service.py:

create_referral_link(user_id: int) -> ReferralLink:
- Unique referral code
- Track signups from link
- Reward system:
  - Referrer: 1 month free per signup
  - Referee: 20% off first month
- Leaderboard for top referrers
- Bonus for milestone referrals

5. Discount & Promo System:

app/services/billing/promo_service.py:

create_promo_code(code: str, config: dict) -> PromoCode:
- Discount types:
  - Percentage off (25% off annual)
  - Fixed amount ($10 off)
  - Free trial extension (30 days)
  - Free addon (extra voice clone)
- Conditions:
  - New customers only
  - Existing plan upgrade only
  - Min commitment (annual)
  - Expiration date
  - Max uses
- Track redemption and revenue impact

6. Feature Adoption Tracking:

app/services/analytics/feature_adoption.py:

track_feature_discovery(user_id: int, feature: str):
- When user first sees feature
- When user first uses feature
- Continued usage frequency
- Feature stickiness metrics
- Correlation with retention

identify_unused_premium_features(user_id: int) -> list[str]:
- Premium user not using premium features
- Send targeted tips/tutorials
- Reduce churn by increasing value perception

7. Customer Success Automation:

app/services/customer_success/automation.py:

onboarding_automation(user_id: int):
- Day 1: Welcome email + getting started guide
- Day 2: Schedule first interview
- Day 3: Voice cloning tutorial
- Day 7: Share with family
- Day 14: Create first compilation
- Day 30: Check-in survey

success_milestones(user_id: int, milestone: str):
- First voice clone created
- 10th memory recorded
- 100 minutes of audio
- First family member invited
- Celebrate with badges/notifications
- Encourage sharing on social

8. Pricing Experiments:

app/services/billing/pricing_experiments.py:

run_pricing_test(variant: str) -> PricingVariant:
- A/B test pricing tiers
- Test annual vs monthly conversion
- Test feature bundling
- Track: conversion rate, ARPU, LTV
- Statistical significance testing
- Auto-winner selection

9. Billing Intelligence:

app/services/billing/intelligence.py:

predict_ltv(user_id: int) -> float:
- Predict lifetime value
- Based on: usage, engagement, plan, features
- Identify high-value users for VIP treatment

optimize_user_plan(user_id: int) -> Recommendation:
- Suggest plan that best fits usage
- "You only use X features, downgrade saves $Y"
- "You're hitting limits, upgrade for $Z"
- Build trust with honest recommendations

detect_payment_risk(user_id: int) -> RiskScore:
- Predict payment failure likelihood
- Update card prompts before billing
- Reduce involuntary churn
- Retry logic optimization

10. Dashboard for Metrics:

packages/frontend/src/app/admin/monetization/page.tsx:
- MRR tracking
- Churn rate
- Conversion funnel (free → trial → paid)
- Feature usage by plan
- Upgrade/downgrade flow
- Promo code performance
- LTV cohorts
- Pricing experiment results
```

---

## 🎯 PREMIUM FEATURES: IMPLEMENTATION CHECKLIST

### Core Subscription System
- [ ] Database schema (subscriptions, plans, usage, payments)
- [ ] Stripe integration (payments, webhooks)
- [ ] Usage tracking & enforcement
- [ ] Plan management (upgrade/downgrade/cancel)
- [ ] Billing portal

### Premium Voice Features
- [ ] Emotional voice cloning
- [ ] Voice blending/mixing
- [ ] SSML support
- [ ] Batch TTS processing
- [ ] Voice variations (aged, emotional)
- [ ] Higher quality audio formats
- [ ] Background music integration
- [ ] Multi-voice narration

### Advanced Memory Features
- [ ] AI story enhancement
- [ ] Memory compilations
- [ ] Emotion detection & adjustment
- [ ] Advanced export formats (WAV, FLAC)
- [ ] Memory versioning
- [ ] Custom pronunciations

### Analytics & Insights
- [ ] Premium analytics dashboard
- [ ] Collection insights
- [ ] Theme analysis
- [ ] Engagement metrics
- [ ] Family activity tracking
- [ ] Custom reports (PDF, PPTX)
- [ ] Real-time analytics stream

### Collaboration Features
- [ ] Granular permissions
- [ ] Comments & reactions
- [ ] Collaborative tagging
- [ ] Shared collections
- [ ] Group interview sessions
- [ ] Family workspace
- [ ] Activity feed
- [ ] Version control

### API & Developer Tools
- [ ] API key management
- [ ] Public REST API
- [ ] SDK generation (Python, JS)
- [ ] Webhook system
- [ ] API documentation
- [ ] Developer portal
- [ ] Rate limiting
- [ ] Usage analytics

### Enterprise Features
- [ ] Custom model training
- [ ] SSO (SAML, OAuth)
- [ ] Audit logs
- [ ] White-label options
- [ ] Dedicated support
- [ ] Custom contracts
- [ ] Advanced security (SOC 2)

### Growth & Monetization
- [ ] Smart upgrade prompts
- [ ] Free trial management
- [ ] Referral program
- [ ] Promo code system
- [ ] Feature adoption tracking
- [ ] Customer success automation
- [ ] Pricing experiments
- [ ] Churn prevention

---

## 💰 PRICING STRATEGY

### Free Tier (Lead Generation)
**Price:** $0/month
- 1 voice clone
- 50 memories max
- 1GB storage
- 10k characters/month TTS
- Standard quality audio
- Basic analytics
- 5 family members

### Premium Tier (Primary Revenue)
**Price:** $29.99/month or $299/year (17% savings)
- 10 voice clones
- 1,000 memories
- 50GB storage
- 500k characters/month TTS
- High-quality audio
- Emotional voices
- Voice blending
- AI story enhancement
- Background music
- Memory compilations
- Advanced analytics
- 25 family members
- Collaboration features
- Priority support
- Basic API access

### Enterprise Tier (High-Value Customers)
**Price:** $99.99/month or $999/year
**Target:** Families with significant wealth, professional biographers, senior living facilities
- Unlimited voice clones
- Unlimited memories
- 500GB storage
- 2M characters/month TTS
- Premium audio (PCM)
- All voice features
- Custom voice models
- White-label option
- Full API access (1000 req/min)
- SSO
- Audit logs
- Dedicated support
- Custom SLA
- On-premise option (future)

### Add-ons (Additional Revenue)
- Extra storage: $5/month per 50GB
- API overage: $0.01 per 1k characters
- Professional voice cloning: $99 one-time (ultra-high quality)
- Custom integrations: $499 one-time
- Professional bio service: $999+ (human + AI combination)

---

## 📊 SUCCESS METRICS

### Subscription Metrics
- **MRR (Monthly Recurring Revenue):** Track monthly
- **ARR (Annual Recurring Revenue):** Track quarterly
- **Churn Rate:** Target <5% monthly
- **Upgrade Rate:** Free → Premium target 10%
- **CAC (Customer Acquisition Cost):** Target <$50
- **LTV (Lifetime Value):** Target >$500
- **LTV:CAC Ratio:** Target >10:1

### Feature Adoption
- % Premium users using voice emotions
- % Premium users creating compilations
- % Premium users using API
- % Enterprise users using SSO
- Average features used per plan

### Engagement Metrics
- Premium users: >5 memories/month
- Enterprise users: >20 memories/month
- Family collaboration: >3 members active
- API usage: >1000 calls/month (Enterprise)

### Financial Targets
- **Year 1:** $50k MRR (1,500 Premium, 50 Enterprise)
- **Year 2:** $150k MRR (4,000 Premium, 200 Enterprise)
- **Year 3:** $500k MRR (12,000 Premium, 800 Enterprise)

---

## 🚀 LAUNCH STRATEGY

### Phase 1: Foundation (Week 13)
1. Build subscription infrastructure
2. Stripe integration + testing
3. Usage tracking system
4. Basic tier enforcement
5. Billing portal MVP

### Phase 2: Premium Features (Weeks 14-15)
1. Roll out voice features (Premium)
2. Launch memory enhancements (Premium)
3. Build analytics dashboard (Premium)
4. Enable collaboration (Premium)
5. Beta test with early adopters

### Phase 3: Enterprise & API (Week 16)
1. Launch public API
2. Build developer portal
3. Release SDKs
4. Enterprise feature rollout
5. SSO integration

### Phase 4: Growth (Ongoing)
1. Optimize conversion funnels
2. A/B test pricing
3. Referral program launch
4. Content marketing (case studies)
5. Partnership outreach

---

## 🎨 MARKETING ANGLES FOR PREMIUM

### Value Propositions
1. **Emotional Depth:** "Preserve not just words, but emotions"
2. **Professional Quality:** "Studio-quality voice clones"
3. **Family Legacy:** "Create audiobooks of your family history"
4. **Time Savings:** "AI enhancement saves hours of editing"
5. **Collaboration:** "Your whole family contributing to one story"
6. **Developer Platform:** "Build custom memory applications"

### Target Segments
1. **Affluent Families:** Willing to pay for quality legacy preservation
2. **Professional Biographers:** Need advanced tools and API access
3. **Senior Living Facilities:** Enterprise accounts, bulk licensing
4. **Genealogy Enthusiasts:** Combine with family tree research
5. **Content Creators:** Use voice cloning for podcasts/videos
6. **Developers:** Build integrations and applications

### Conversion Tactics
1. **Free Trial:** 14 days Premium, no credit card
2. **Freemium Limits:** Hit limits → upgrade prompt
3. **Feature Discovery:** Show locked premium features in-app
4. **Social Proof:** Testimonials from families
5. **FOMO:** "Limited time: Save 20% on annual"
6. **Bundles:** "Gift Premium to your family"