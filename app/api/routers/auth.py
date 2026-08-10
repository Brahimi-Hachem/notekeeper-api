from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.auth import Token, UserCreate, UserResponse
from app.services.auth import (
    authenticate_user,
    create_user,
    get_user_by_email,
)

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def register(
    user_data: UserCreate,
    db: Annotated[Session, Depends(get_db)],
):
    existing_user = get_user_by_email(
        db,
        user_data.email,
    )

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    return create_user(
        db,
        user_data,
    )


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    request: Request,
    db: Annotated[Session, Depends(get_db)],
):
    if request.headers.get("content-type", "").startswith(
        "application/x-www-form-urlencoded"
    ):
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
    else:
        body = await request.json()
        username = body.get("email")
        password = body.get("password")

    if not username or not password:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Email and password are required.",
        )

    user = authenticate_user(
        db,
        username,
        password,
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    access_token = create_access_token(
        subject=str(user.id),
        expires_delta=timedelta(
            minutes=30,
        ),
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }
