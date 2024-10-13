import logging

from sqlalchemy import insert

from apps.common.kafka.dto import CompletedTaskDTO
from apps.todo_monitor.infra.db.connection import db
from apps.todo_monitor.infra.db.models import CompletedTaskOrm

logger = logging.getLogger(__name__)


class CounterCompletedTaskHandlerService:

    async def process(self, msg: CompletedTaskDTO) -> None:
        logger.debug(f"AAA {msg}")
        async with db.session_scope() as session:
            stmt = (insert(CompletedTaskOrm).values(user_id=msg.user_id)).returning(CompletedTaskOrm)
            row = (await session.execute(stmt)).first()
        logger.debug(f"AAA {row}")
