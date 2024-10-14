from uuid import UUID

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from apps.todo_monitor.infra.db.models import UserTaskOrm


class UserTaskRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def get_by_user_id_or_none(self, user_id: int) -> UserTaskOrm | None:
        stmt = select(UserTaskOrm).where(UserTaskOrm.user_id == user_id)
        row = await self._session.scalar(stmt)
        return row

    async def create(self, user_id: int) -> UserTaskOrm:
        stmt = (insert(UserTaskOrm).values(user_id=user_id)).returning(UserTaskOrm)
        row = (await self._session.execute(stmt)).first()
        return row[0]  # type:ignore[index]

    async def update_successful_count_task(self, id_: UUID, сount_: int) -> None:
        stmt = update(UserTaskOrm).where(UserTaskOrm.id == id_).values(successful_count=сount_)
        await self._session.execute(stmt)

    async def update_failed_count_task(self, id_: UUID, сount_: int) -> None:
        stmt = update(UserTaskOrm).where(UserTaskOrm.id == id_).values(failed_count=сount_)
        await self._session.execute(stmt)
