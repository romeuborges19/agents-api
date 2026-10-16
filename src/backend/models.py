import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    hashed_password: Mapped[str]

    sessions: Mapped[List["Session"]] = relationship(back_populates="user")
    messages: Mapped[List["Message"]] = relationship(back_populates="user")


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    subject: Mapped[str]

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="sessions")
    messages: Mapped[List["Message"]] = relationship(back_populates="session")


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str]

    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("sessions.id"))
    session: Mapped["Session"] = relationship(back_populates="messages")

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    user: Mapped["User"] = relationship(back_populates="messages")

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())
