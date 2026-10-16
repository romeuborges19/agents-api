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


class SessionCreate(BaseModel):
    subject: str
    car_id: int


class CarCreate(BaseModel):
    name: str
    description: str


class CarSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
