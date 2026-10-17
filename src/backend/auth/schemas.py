from pydantic import BaseModel, ConfigDict


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
