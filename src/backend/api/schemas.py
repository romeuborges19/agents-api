from pydantic import BaseModel, ConfigDict


class AgentInput(BaseModel):
    input: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str


class UserInDB(UserSchema):
    model_config = ConfigDict(from_attributes=True)

    hashed_password: str


class UserCreate(BaseModel):
    name: str
    password: str


class SessionSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str
    car: CarSchema


class SessionPreviewSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    subject: str


class MessageSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    content: str
    user: UserSchema | None


class SessionWithMessages(SessionSchema):
    model_config = ConfigDict(from_attributes=True)

    messages: list[MessageSchema]


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


class CarWithSession(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    session: SessionPreviewSchema | None
