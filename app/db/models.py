from typing import Optional

import enum
from sqlalchemy import Enum
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String, unique=True, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String)


class TaskStatus(enum.Enum):
    ASSIGNED = "assigned"
    RESOLVED = "resolved"
    CLOSED = "closed"
    FEEDBACK = "feedback"
    REJECTED = "rejected"


class Task(Base):
    __tablename__ = 'tasks'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    complete: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String, nullable=False, default="assigned")  # TODO: added using TaskStatus

    photos: Mapped["Photo"] = relationship("Photo", back_populates="task")


class Photo(Base):
    __tablename__ = 'photos'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String, index=True)  # Название файла в MinIO
    url: Mapped[str] = mapped_column(String)  # Ссылка на фото в MinIO
    task_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("tasks.id"))  # Связь с таблицей заданий

    task: Mapped[Task] = relationship("Task", back_populates="photos")

