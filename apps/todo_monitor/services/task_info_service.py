import logging
from datetime import datetime

from apps.common.kafka.dto import CompletedTaskDTO
from apps.todo_monitor.infra.db.connection import db
from apps.todo_monitor.infra.db.models import InfoTaskOrm
from apps.todo_monitor.infra.repositories.info_task import InfoTaskRepository
from apps.todo_monitor.services.service_abc import AbstractHandlerServiceKafka

logger = logging.getLogger(__name__)


class TaskInfoHandlerService(AbstractHandlerServiceKafka):

    def __init__(self) -> None:
        self._repo = InfoTaskRepository

    async def process(self, data: CompletedTaskDTO) -> None:
        task_info = await self._get_or_create(data)
        await self._update_task_completed_ad(task_info, data)

    async def _get_or_create(self, data: CompletedTaskDTO) -> InfoTaskOrm:
        async with db.session_scope() as session:
            if not (result := await self._repo(session).get_by_task_id_or_none(data.task_id)):
                result = await self._repo(session).create(data)
                logger.debug(f"Created new task-info: user_id={result.user_id}, task_id={result.task_id}")
        return result

    async def _update_task_completed_ad(self, task_info: InfoTaskOrm, data: CompletedTaskDTO) -> None:
        completed_at_datetime = datetime.fromisoformat(data.completed_at).replace(tzinfo=None)
        async with db.session_scope() as session:
            await self._repo(session).update(id_=task_info.id, completed_at=completed_at_datetime)
        logger.debug(f"user_id={task_info.user_id} updated task field completed_at={completed_at_datetime}")


def get_task_info_service() -> AbstractHandlerServiceKafka:
    return TaskInfoHandlerService()
