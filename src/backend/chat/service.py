from sqlalchemy.orm import Session as DBSession

from backend.chat.models import Car, Session
from backend.chat.schemas import (
    CarCreate,
    CarSchema,
    CarWithSession,
    SessionPreviewSchema,
    SessionSchema,
    SessionWithMessages,
    UserSchema,
)


def get_cars(db: DBSession) -> list[CarWithSession]:
    cars = Car.get_cars(db)
    return [
        CarWithSession(
            id=c.id,
            name=c.name,
            description=c.description,
            session=SessionPreviewSchema.model_validate(c.sessions[0])
            if c.sessions
            else None,
        )
        for c in cars
    ]


def create_car(db: DBSession, new_car: CarCreate) -> CarSchema:
    car_obj = Car(name=new_car.name, description=new_car.description)
    db.add(car_obj)
    db.commit()
    return CarSchema.model_validate(car_obj)


def get_sessions(db: DBSession, user: UserSchema) -> list[SessionSchema]:
    sessions = Session.get_sessions(db, user)
    return [SessionSchema.model_validate(s) for s in sessions]


def create_session(db: DBSession, user: UserSchema, car_id: int) -> SessionSchema:
    car = Car.get_by_id(db, car_id)

    if car.sessions:
        return SessionSchema.model_validate(car.sessions[0])

    session_obj = Session(subject=car.name, car_id=car.id, user_id=user.id)
    db.add(session_obj)
    db.commit()

    return SessionSchema.model_validate(session_obj)


def retrieve_messages(db: DBSession, car_id: int):
    session = Session.get_with_messages(db, car_id)
    return SessionWithMessages.model_validate(session)
