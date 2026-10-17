from typing import Annotated

from dotenv import load_dotenv
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.auth.dependencies import get_current_active_user
from backend.chat import service
from backend.chat.ai.agent import PersonalAgent
from backend.chat.schemas import AgentInput, CarCreate, UserSchema
from backend.core.database import get_db

load_dotenv()

router = APIRouter()


@router.get("/cars")
async def get_cars(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return service.get_cars(db)


@router.post("/cars")
async def create_car(
    new_car: CarCreate,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return service.create_car(db, new_car)


@router.get("/sessions")
async def get_sessions(
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return service.get_sessions(db, current_user)


@router.post("/cars/{car_id}/sessions")
async def create_session(
    car_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return service.create_session(db, current_user, car_id)


@router.get("/cars/{car_id}/messages")
async def retrieve_messages(
    car_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    return service.retrieve_messages(db, car_id)


@router.post("/cars/{car_id}/messages")
async def create_message(
    input: AgentInput,
    car_id: int,
    db: Annotated[Session, Depends(get_db)],
    current_user: Annotated[UserSchema, Depends(get_current_active_user)],
):
    session = service.retrieve_messages(db, car_id)
    agent = PersonalAgent(session_state={"car": session.car.model_dump()})
    return agent.query(input.input, current_user.id, session.id)
