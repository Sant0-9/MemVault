from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_token

security = HTTPBearer()


async def get_db() -> Generator:
    pass


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> str:
    token = credentials.credentials
    user_id = verify_token(token)
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )
    return user_id


async def require_admin(current_user: str = Depends(get_current_user)) -> str:
    return current_user


def pagination_params(
    page: int = 1,
    size: int = 20,
    sort_by: Optional[str] = None,
    order: str = "desc",
):
    if page < 1:
        page = 1
    if size < 1 or size > 100:
        size = 20
    if order not in ["asc", "desc"]:
        order = "desc"

    return {
        "skip": (page - 1) * size,
        "limit": size,
        "sort_by": sort_by,
        "order": order,
    }
