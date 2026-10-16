from sqlalchemy.orm import Session as DBSession

from backend.api.schemas import (
    CarCreate,
    CarSchema,
    SessionCreate,
    SessionSchema,
    SessionWithMessages,
    UserSchema,
)
from backend.models import Car, Session


class CarService:
    def __init__(self, db: DBSession):
        self.db = db

    def get_cars(self) -> list[CarSchema]:
        cars = Car.get_cars(self.db)
        return [CarSchema.model_validate(c) for c in cars]

    def create_car(self, new_car: CarCreate) -> CarSchema:
        car_obj = Car(name=new_car.name, description=new_car.description)
        self.db.add(car_obj)
        self.db.commit()
        return CarSchema.model_validate(car_obj)


class SessionService:
    def __init__(self, db: DBSession):
        self.db = db

    def get_sessions(self, user: UserSchema) -> list[SessionSchema]:
        sessions = Session.get_sessions(self.db, user)
        return [SessionSchema.model_validate(s) for s in sessions]

    def create_session(self, user: UserSchema, car_id: int) -> SessionSchema:
        car = Car.get_by_id(self.db, car_id)

        if car.sessions:
            return SessionSchema.model_validate(car.sessions[0])

        session_obj = Session(subject=car.name, car_id=car.id, user_id=user.id)
        self.db.add(session_obj)

        self.db.commit()

        return SessionSchema.model_validate(session_obj)

    def retrieve_messages(self, car_id: int):
        session = Session.get_with_messages(self.db, car_id)
        return SessionWithMessages.model_validate(session)
