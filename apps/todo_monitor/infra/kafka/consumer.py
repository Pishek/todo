import json
import logging
from typing import Any

from aiokafka import AIOKafkaConsumer
from aiokafka.structs import ConsumerRecord

from apps.common.kafka.dto import CompletedTaskDTO
from apps.common.kafka.enums import TopicKafkaEnum
from apps.todo_monitor.config import settings
from apps.todo_monitor.services.counter_service import CounterCompletedTaskHandlerService

logger = logging.getLogger(__name__)

aiokafka_logger = logging.getLogger("aiokafka")
aiokafka_logger.setLevel(logging.INFO)


class KafkaConsumer:
    def __init__(self, topics: list[str]) -> None:
        self._topics = topics
        self._consumer = AIOKafkaConsumer(
            *self._topics,
            bootstrap_servers=f"{settings.KAFKA.HOST}:{settings.KAFKA.PORT}",
            group_id=settings.KAFKA.GROUP_ID,
        )
        self._counter_service = CounterCompletedTaskHandlerService()

    async def process_loop(self) -> None:
        try:
            await self._consumer.start()
            async for msg in self._consumer:
                if msg is None:
                    continue

                topic = msg.topic
                msg = self._deserialize_message(msg)

                if topic == TopicKafkaEnum.COMPLETED_TASKS:
                    msg_dto = self._build_completed_task_dto(msg)
                    await self._counter_service.process(msg_dto)

        finally:
            await self._consumer.stop()

    def _build_completed_task_dto(self, msg: dict[str, Any]) -> CompletedTaskDTO:
        return CompletedTaskDTO(**msg)

    def _deserialize_message(self, msg: ConsumerRecord) -> dict[str, Any]:
        logger.debug(
            f"Received message from topic: {msg.topic}, partition: {msg.partition}, "
            f"offset: {msg.offset}, key: {msg.key}, value: {msg.value.decode('utf-8')}"
        )
        return json.loads(msg.value.decode("utf-8"))


def get_completed_consumer() -> KafkaConsumer:
    return KafkaConsumer(topics=[TopicKafkaEnum.COMPLETED_TASKS])
