from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_active_user
from backend.auth.schemas import Token, UserCreate, UserSchema
from backend.auth.service import (
    authenticate_user,
    create_access_token,
    create_user,
)
from backend.core.database import get_db
from backend.core.settings import settings

auth_router = APIRouter()


@auth_router.post("/users")
async def new_user(
    user: UserCreate, db: Annotated[Session, Depends(get_db)]
) -> UserSchema:
    return create_user(db, user)


@auth_router.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
) -> Token:
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@auth_router.get("/users/me/")
async def read_users_me(
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
) -> UserSchema:
    return current_user
