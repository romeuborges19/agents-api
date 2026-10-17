from sqlalchemy.orm import Session as DBSession

from backend.auth.schemas import UserSchema
from backend.chat.ai.agent import CarAgentResponse, PersonalAgent
from backend.chat.models import Car, Message, Session
from backend.chat.schemas import CarDescription


def _create_message(
    db: DBSession, content: str, session: Session, user_id: int | None = None
):
    message = Message(user_id=user_id, session_id=session.id, content=content)
    db.add(message)
    db.flush()


def query(db: DBSession, user: UserSchema, car_id: int, input: str) -> CarAgentResponse:
    car = Car.get_by_id(db, car_id)
    session = car.sessions[0]
    refered_car = CarDescription.model_validate(car)
    agent = PersonalAgent(session_state={"car": refered_car.model_dump()})

    _create_message(db, user_id=user.id, session=session, content=input)
    response = agent.query(input, user.id, session.id)

    _create_message(db, content=response.response, session=session)
    db.commit()
    return response
