from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.common.kafka.dto import CompletedTaskDTO
from apps.todo_monitor.infra.db.models import InfoTaskOrm


class InfoTaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def get_by_task_id_or_none(self, task_id: int) -> InfoTaskOrm | None:
        stmt = select(InfoTaskOrm).where(InfoTaskOrm.task_id == task_id)
        row = await self._session.scalar(stmt)
        return row

    async def create(self, data: CompletedTaskDTO) -> InfoTaskOrm:
        stmt = (
            insert(InfoTaskOrm).values(
                task_id=data.task_id,
                user_id=data.user_id,
                title=data.title,
                created_at=datetime.fromisoformat(data.created_at).replace(tzinfo=None),
                completed_at=datetime.fromisoformat(data.completed_at).replace(tzinfo=None),
            )
        ).returning(InfoTaskOrm)
        row = (await self._session.execute(stmt)).first()
        return row[0]  # type:ignore[index]

    async def update(self, id_: UUID, **kwargs: Any) -> None:
        stmt = update(InfoTaskOrm).where(InfoTaskOrm.id == id_).values(**kwargs)
        await self._session.execute(stmt)
