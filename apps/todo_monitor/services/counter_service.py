import logging
from uuid import uuid4

from sqlalchemy import select

from apps.common.kafka.dto import CompletedTaskDTO
from apps.todo_monitor.infra.db.connection import db
from apps.todo_monitor.models import CompletedTaskOrm

logger = logging.getLogger(__name__)


class CounterCompletedTaskHandlerService:

    def process(self, msg: CompletedTaskDTO) -> None:
        logger.debug(f"AAA {msg}")
        with db.session_scope() as session:
            stmt = select(CompletedTaskOrm).where(CompletedTaskOrm.id == uuid4())
            row = session.scalars(stmt).first()
