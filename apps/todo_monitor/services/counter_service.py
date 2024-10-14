import logging

from apps.common.kafka.dto import CompletedTaskDTO
from apps.todo_monitor.infra.db.connection import db
from apps.todo_monitor.infra.db.models import UserTaskOrm
from apps.todo_monitor.infra.repositories.completed_task import UserTaskRepository
from apps.todo_monitor.services.service_abc import AbstractHandlerServiceKafka

logger = logging.getLogger(__name__)


class CounterCompletedTaskHandlerService(AbstractHandlerServiceKafka):

    def __init__(self) -> None:
        self._repo = UserTaskRepository
        self._max_day_task = 3  # максимальный дедлайн в кол-ве дней на выполнение одной задачи

    async def process(self, data: CompletedTaskDTO) -> None:
        user_info = await self._get_or_create(data.user_id)

        if data.duration_in_days > self._max_day_task:
            await self._handle_failed_task(user_info)
        else:
            await self._handle_successful_task(user_info)

    async def _get_or_create(self, user_id: int) -> UserTaskOrm:
        async with db.session_scope() as session:
            if not (result := await self._repo(session).get_by_user_id_or_none(user_id)):
                result = await self._repo(session).create(user_id=user_id)
                logger.debug(f"Created new user: user_id={result.user_id}")
        return result

    async def _handle_failed_task(self, user_info: UserTaskOrm) -> None:
        new_count = user_info.failed_count + 1
        async with db.session_scope() as session:
            await self._repo(session).update_failed_count_task(user_info.id, new_count)
        logger.debug(f"user_id={user_info.user_id} updated failed_count_tasks={new_count}")

    async def _handle_successful_task(self, user_info: UserTaskOrm) -> None:
        new_count = user_info.successful_count + 1
        async with db.session_scope() as session:
            await self._repo(session).update_successful_count_task(user_info.id, new_count)
        logger.debug(f"user_id={user_info.user_id} updated successful_count_tasks={new_count}")


def get_counter_service() -> AbstractHandlerServiceKafka:
    return CounterCompletedTaskHandlerService()
