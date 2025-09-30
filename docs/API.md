# API Documentation

Base URL: `http://localhost:8000/api/v1`

## Authentication

All protected endpoints require a JWT token in the Authorization header:

```
Authorization: Bearer <token>
```

### Get Access Token

**POST** `/auth/login`

Request:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "token_type": "bearer"
}
```

## Health Checks

### Basic Health Check

**GET** `/health`

Response:
```json
{
  "status": "healthy",
  "app_name": "MemoryVault",
  "version": "0.1.0",
  "environment": "development"
}
```

### Readiness Check

**GET** `/health/ready`

Response:
```json
{
  "status": "ready",
  "checks": {
    "database": "ok",
    "redis": "ok"
  }
}
```

## Elders

### List Elders

**GET** `/elders`

Query Parameters:
- `page` (optional): Page number (default: 1)
- `size` (optional): Page size (default: 20)
- `search` (optional): Search query
- `sort_by` (optional): Field to sort by
- `order` (optional): asc or desc (default: desc)

Response:
```json
{
  "items": [
    {
      "id": 1,
      "name": "John Doe",
      "date_of_birth": "1945-06-15",
      "hometown": "Chicago, IL",
      "created_at": "2025-01-15T10:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20,
  "pages": 1
}
```

### Get Elder

**GET** `/elders/{elder_id}`

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "date_of_birth": "1945-06-15",
  "hometown": "Chicago, IL",
  "current_location": "Miami, FL",
  "email": "john@example.com",
  "phone": "+1-555-0123",
  "bio": "Veteran, retired teacher",
  "memory_count": 45,
  "total_duration": 12600,
  "created_at": "2025-01-15T10:00:00Z"
}
```

### Create Elder

**POST** `/elders`

Request:
```json
{
  "name": "John Doe",
  "date_of_birth": "1945-06-15",
  "hometown": "Chicago, IL",
  "email": "john@example.com",
  "phone": "+1-555-0123",
  "bio": "Veteran, retired teacher"
}
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "created_at": "2025-01-15T10:00:00Z"
}
```

### Update Elder

**PUT** `/elders/{elder_id}`

Request:
```json
{
  "current_location": "Miami, FL",
  "bio": "Updated bio"
}
```

### Delete Elder

**DELETE** `/elders/{elder_id}`

Response:
```json
{
  "success": true,
  "message": "Elder deleted successfully"
}
```

## Memories

### List Memories

**GET** `/memories`

Query Parameters:
- `elder_id` (optional): Filter by elder
- `category` (optional): Filter by category
- `era` (optional): Filter by era
- `search` (optional): Full-text search
- `page`, `size`, `sort_by`, `order`: Pagination

Response:
```json
{
  "items": [
    {
      "id": 1,
      "elder_id": 1,
      "title": "Meeting My Wife",
      "summary": "Story about meeting his wife at a dance",
      "duration_seconds": 180,
      "category": "love-relationships",
      "era": "1960s",
      "created_at": "2025-01-15T11:00:00Z"
    }
  ],
  "total": 1,
  "page": 1,
  "size": 20,
  "pages": 1
}
```

### Get Memory

**GET** `/memories/{memory_id}`

Response:
```json
{
  "id": 1,
  "elder_id": 1,
  "title": "Meeting My Wife",
  "transcription": "Full transcription...",
  "summary": "Short summary...",
  "audio_url": "https://gateway.pinata.cloud/...",
  "duration_seconds": 180,
  "category": "love-relationships",
  "era": "1960s",
  "tags": ["romance", "dance", "1960s"],
  "people_mentioned": ["Mary", "Bob"],
  "location": "Chicago, IL",
  "sentiment": "joyful",
  "historical_context": "In 1965...",
  "created_at": "2025-01-15T11:00:00Z"
}
```

### Create Memory

**POST** `/memories`

Request (multipart/form-data):
```
elder_id: 1
title: "Meeting My Wife"
category: "love-relationships"
audio: [file]
```

Response:
```json
{
  "id": 1,
  "status": "processing",
  "message": "Memory created and queued for processing"
}
```

### Update Memory

**PUT** `/memories/{memory_id}`

Request:
```json
{
  "title": "Updated Title",
  "category": "love-relationships",
  "tags": ["romance", "dance"]
}
```

### Delete Memory

**DELETE** `/memories/{memory_id}`

## Interview Sessions

### Start Interview

**POST** `/interviews/start`

Request:
```json
{
  "elder_id": 1
}
```

Response:
```json
{
  "session_id": "abc123",
  "opening_question": "Can you tell me about your childhood home?"
}
```

### Get Next Question

**POST** `/interviews/{session_id}/next`

Request:
```json
{
  "response": "User's audio transcription or text response"
}
```

Response:
```json
{
  "question": "What was your favorite room in the house?",
  "should_continue": true,
  "fatigue_level": 0.2
}
```

### End Interview

**POST** `/interviews/{session_id}/end`

Response:
```json
{
  "session_id": "abc123",
  "duration_seconds": 1800,
  "memories_created": 5,
  "completeness_score": 0.85
}
```

## Error Responses

All errors follow this format:

```json
{
  "success": false,
  "error": "Error message",
  "detail": "Detailed error information",
  "request_id": "abc-123-def"
}
```

Common HTTP Status Codes:
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `500` - Internal Server Error

## Rate Limiting

- Default: 100 requests per minute per IP
- Authenticated: 1000 requests per minute per user

Rate limit headers:
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 99
X-RateLimit-Reset: 1640000000
```
