from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import DateTime, Integer, MetaData, text
from sqlalchemy.dialects.postgresql import TEXT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata


class UserTaskOrm(Base):
    __tablename__ = "user_tasks"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, server_default=text("gen_random_uuid()"))
    user_id: Mapped[int] = mapped_column(Integer, comment="id пользователя")
    successful_count: Mapped[int] = mapped_column(Integer, comment="Количество успешных выполненых задач", default=0)
    failed_count: Mapped[int] = mapped_column(Integer, comment="Количество проваленных задач", default=0)


class InfoTaskOrm(Base):
    __tablename__ = "info_tasks"
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, server_default=text("gen_random_uuid()"))
    task_id: Mapped[int] = mapped_column(Integer, comment="Номер задачи")
    user_id: Mapped[int] = mapped_column(Integer, comment="id пользователя")
    title: Mapped[str] = mapped_column(TEXT, comment="Название задачи")
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="время создания задачи")
    completed_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, comment="время закрытия задачи")
    completion_attempts: Mapped[int] = mapped_column(Integer, default=0, comment="Попытка завершить задачу")
