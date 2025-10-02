"""API router for version 1 endpoints."""

from fastapi import APIRouter

from app.api.v1.endpoints import (
    audio,
    auth,
    elders,
    family_members,
    interviews,
    memories,
)

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(elders.router, prefix="/elders", tags=["elders"])
api_router.include_router(memories.router, prefix="/memories", tags=["memories"])
api_router.include_router(
    family_members.router, prefix="/family-members", tags=["family-members"]
)
api_router.include_router(interviews.router, prefix="/interviews", tags=["interviews"])
api_router.include_router(audio.router, prefix="/audio", tags=["audio"])
