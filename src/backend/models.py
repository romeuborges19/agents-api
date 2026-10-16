import datetime
from typing import List

from sqlalchemy import DateTime, ForeignKey, Integer, func, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    selectinload,
)
from sqlalchemy.orm import Session as DBSession


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
    messages: Mapped[List["Message"]] = relationship(
        back_populates="session", order_by="(Message.created_at, Message.id)"
    )

    car_id: Mapped[int] = mapped_column(Integer, ForeignKey("cars.id"))
    car: Mapped["Car"] = relationship(back_populates="sessions")

    @staticmethod
    def get_sessions(db: DBSession, user):
        stmt = select(Session).filter_by(user_id=user.id)
        return db.scalars(stmt).all()

    @staticmethod
    def get_by_id(db, id: int) -> Session:
        stmt = select(Session).filter_by(id=id)
        return db.scalars(stmt).first()

    @staticmethod
    def get_with_messages(db, car_id: int) -> Session:
        stmt = (
            select(Session)
            .filter_by(car_id=car_id)
            .options(selectinload(Session.messages))
        )
        return db.scalars(stmt).first()


class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    content: Mapped[str]

    session_id: Mapped[int] = mapped_column(Integer, ForeignKey("sessions.id"))
    session: Mapped["Session"] = relationship(back_populates="messages")

    user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    user: Mapped["User"] = relationship(back_populates="messages")

    created_at: Mapped[datetime.datetime] = mapped_column(DateTime, default=func.now())


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    description: Mapped[str]

    sessions: Mapped[List["Session"]] = relationship(back_populates="car")

    @staticmethod
    def get_cars(db) -> list[Car]:
        stmt = select(Car).options(selectinload(Car.sessions))
        return db.scalars(stmt).all()

    @staticmethod
    def get_by_id(db, id: int) -> Car:
        stmt = select(Car).filter_by(id=id)
        return db.scalars(stmt).first()
