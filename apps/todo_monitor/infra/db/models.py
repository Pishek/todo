from uuid import UUID, uuid4

from sqlalchemy import Integer, MetaData, text
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
