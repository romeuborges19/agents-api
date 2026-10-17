from pydantic import BaseModel, ConfigDict

from backend.auth.schemas import UserSchema


class AgentInput(BaseModel):
    input: str


class SessionCreate(BaseModel):
    car_id: int


class CarCreate(BaseModel):
    name: str
    description: str


class CarDescription(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    description: str


class CarSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str


class SessionPreviewSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str


class CarWithSession(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    session: SessionPreviewSchema | None


class SessionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    car: CarSchema


class MessageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    user: UserSchema | None


class SessionWithMessages(SessionSchema):
    model_config = ConfigDict(from_attributes=True)

    messages: list[MessageSchema]
