from datetime import datetime, timedelta, timezone

import jwt
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.auth.models import User
from backend.auth.schemas import UserCreate, UserInDB, UserSchema
from backend.core.settings import settings

password_hash = PasswordHash.recommended()


def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)


def get_password_hash(password):
    return password_hash.hash(password)


def get_user(db: Session, username: str):
    stmt = select(User).filter_by(name=username)
    user_obj = db.scalars(stmt).first()
    if not user_obj:
        return None
    return UserInDB.model_validate(user_obj)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, settings.secret_key, algorithm=settings.algorithm
    )
    return encoded_jwt


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    user_obj = User(name=user.name, hashed_password=hashed_password)
    db.add(user_obj)
    db.commit()
    return UserSchema.model_validate(user_obj)
