"""Interview session endpoints."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_db
from app.db.models import Elder, InterviewSession
from app.schemas.interview_session_schema import (
    InterviewQuestionRequest,
    InterviewQuestionResponse,
    InterviewResponseAcknowledge,
    InterviewResponseSubmit,
    InterviewSessionCreate,
    InterviewSessionList,
    InterviewSessionResponse,
    InterviewSessionUpdate,
)
from app.services.openai_service import openai_service

router = APIRouter()


@router.post(
    "/", response_model=InterviewSessionResponse, status_code=status.HTTP_201_CREATED
)
async def create_interview_session(
    session_data: InterviewSessionCreate, db: AsyncSession = Depends(get_db)
) -> Any:
    """Create a new interview session."""
    result = await db.execute(select(Elder).where(Elder.id == session_data.elder_id))
    elder = result.scalar_one_or_none()

    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Elder not found"
        )

    session = InterviewSession(
        elder_id=session_data.elder_id,
        user_id=1,
        title=session_data.title or f"Interview with {elder.name}",
        topic=session_data.topic,
        notes=session_data.notes,
        status="active",
        conversation_history={"turns": []},
        total_questions=0,
        total_responses=0,
    )

    db.add(session)
    await db.commit()
    await db.refresh(session)

    return session


@router.get("/", response_model=InterviewSessionList)
async def list_interview_sessions(
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    elder_id: int | None = Query(None),
    status_filter: str | None = Query(None, alias="status"),
    db: AsyncSession = Depends(get_db),
) -> Any:
    """List interview sessions with pagination and filtering."""
    query = select(InterviewSession).where(InterviewSession.deleted_at.is_(None))

    if elder_id:
        query = query.where(InterviewSession.elder_id == elder_id)

    if status_filter:
        query = query.where(InterviewSession.status == status_filter)

    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    query = query.order_by(InterviewSession.created_at.desc())
    query = query.offset((page - 1) * size).limit(size)

    result = await db.execute(query)
    sessions = list(result.scalars().all())

    return InterviewSessionList(
        items=sessions,  # type: ignore[arg-type]
        total=total,
        page=page,
        size=size,
        pages=(total + size - 1) // size,
    )


@router.get("/{session_id}", response_model=InterviewSessionResponse)
async def get_interview_session(
    session_id: int, db: AsyncSession = Depends(get_db)
) -> Any:
    """Get a specific interview session."""
    result = await db.execute(
        select(InterviewSession).where(
            InterviewSession.id == session_id, InterviewSession.deleted_at.is_(None)
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found"
        )

    return session


@router.patch("/{session_id}", response_model=InterviewSessionResponse)
async def update_interview_session(
    session_id: int,
    session_update: InterviewSessionUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Update an interview session."""
    result = await db.execute(
        select(InterviewSession).where(
            InterviewSession.id == session_id, InterviewSession.deleted_at.is_(None)
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found"
        )

    update_data = session_update.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(session, field, value)

    if session_update.status == "completed" and not session.completed_at:
        session.completed_at = datetime.utcnow()

        if session.started_at:
            duration = (datetime.utcnow() - session.started_at).total_seconds() / 60
            session.duration_minutes = int(duration)

    await db.commit()
    await db.refresh(session)

    return session


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_interview_session(
    session_id: int, db: AsyncSession = Depends(get_db)
) -> None:
    """Soft delete an interview session."""
    result = await db.execute(
        select(InterviewSession).where(
            InterviewSession.id == session_id, InterviewSession.deleted_at.is_(None)
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found"
        )

    session.deleted_at = datetime.utcnow()
    await db.commit()


@router.post("/{session_id}/question", response_model=InterviewQuestionResponse)
async def get_next_question(
    session_id: int,
    request: InterviewQuestionRequest,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Get the next AI-generated interview question."""
    result = await db.execute(
        select(InterviewSession).where(
            InterviewSession.id == session_id, InterviewSession.deleted_at.is_(None)
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found"
        )

    if session.status != "active":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interview session is not active",
        )

    elder_result = await db.execute(select(Elder).where(Elder.id == session.elder_id))
    elder = elder_result.scalar_one_or_none()

    if not elder:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Elder not found"
        )

    conversation_history = session.conversation_history.get("turns", [])  # type: ignore[union-attr]

    question = await openai_service.generate_interview_question(
        elder_name=elder.name,
        conversation_history=conversation_history,
        topic=request.topic,
    )

    conversation_history.append(
        {
            "role": "assistant",
            "content": question,
            "timestamp": datetime.utcnow().isoformat(),
        }
    )

    session.conversation_history = {"turns": conversation_history}  # type: ignore[assignment]
    session.total_questions += 1

    await db.commit()
    await db.refresh(session)

    return InterviewQuestionResponse(question=question, session_id=session.id)


@router.post("/{session_id}/response", response_model=InterviewResponseAcknowledge)
async def submit_interview_response(
    session_id: int,
    response_data: InterviewResponseSubmit,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """Submit user's response to an interview question."""
    result = await db.execute(
        select(InterviewSession).where(
            InterviewSession.id == session_id, InterviewSession.deleted_at.is_(None)
        )
    )
    session = result.scalar_one_or_none()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Interview session not found"
        )

    conversation_history = session.conversation_history.get("turns", [])  # type: ignore[union-attr]

    conversation_history.append(
        {
            "role": "user",
            "content": response_data.response,
            "timestamp": datetime.utcnow().isoformat(),
            "audio_cid": response_data.audio_cid,
        }
    )

    session.conversation_history = {"turns": conversation_history}  # type: ignore[assignment]
    session.total_responses += 1

    await db.commit()
    await db.refresh(session)

    return InterviewResponseAcknowledge(
        success=True,
        message="Response recorded successfully",
        next_question=None,
    )
