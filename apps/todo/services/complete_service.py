import math
from datetime import datetime

from apps.common.kafka.dto import CompletedTaskDTO
from apps.todo.infra.kafka.producer import get_kafka_producer
from apps.todo.models import StatusEnum, TaskOrm


class CompleteTaskService:
    def __init__(self, task: TaskOrm) -> None:
        self._task = task
        self._kafka_producer = get_kafka_producer()

    def process(self) -> TaskOrm:
        self._task.status = StatusEnum.COMPLETED
        self._task.completed_at = datetime.now(tz=self._task.created_at.tzinfo)

        time_difference = self._task.completed_at - self._task.created_at
        self._task.duration_in_days = math.ceil(time_difference.total_seconds() / (60 * 60 * 24))
        self._task.save()

        self._send_message(self._task)
        return self._task

    def _send_message(self, task: TaskOrm) -> None:
        data = CompletedTaskDTO(
            user_id=task.user.pk,
            task_id=task.pk,
            title=task.title,
            priority=task.priority,
            status=task.status,
            created_at=task.created_at.isoformat(),
            completed_at=task.completed_at.isoformat(),
            duration_in_days=task.duration_in_days,
        )
        self._kafka_producer.send_completed_task(message=data)
