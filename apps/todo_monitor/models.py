from uuid import UUID, uuid4

from sqlalchemy import Integer, MetaData, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata = MetaData()


class Base(DeclarativeBase):
    metadata = metadata


class CompletedTaskOrm(Base):
    __tablename__ = "completed_task"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4, server_default=text("uuid_generate_v4()"))
    user_id: Mapped[int] = mapped_column(Integer, comment="id пользователя")
