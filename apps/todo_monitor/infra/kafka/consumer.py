import json
import logging
from typing import Any

from aiokafka import AIOKafkaConsumer
from aiokafka.structs import ConsumerRecord

from apps.common.kafka.dto import CompletedTaskDTO
from apps.common.kafka.enums import TopicKafkaEnum
from apps.todo_monitor.config import settings
from apps.todo_monitor.services.service_abc import AbstractHandlerServiceKafka

logger = logging.getLogger(__name__)

aiokafka_logger = logging.getLogger("aiokafka")
aiokafka_logger.setLevel(logging.INFO)


class KafkaConsumer:
    def __init__(self, name: str, group_id: str, topics: list[str], service: AbstractHandlerServiceKafka) -> None:
        self._name = name
        self._group_id = group_id
        self._topics = topics
        self._consumer = AIOKafkaConsumer(
            *self._topics,
            bootstrap_servers=[
                f"{settings.KAFKA.HOST_1}:{settings.KAFKA.PORT_1}",
                f"{settings.KAFKA.HOST_2}:{settings.KAFKA.PORT_2}",
            ],
            group_id=self._group_id,
            auto_offset_reset="latest",
        )
        self._service = service

    async def process_loop(self) -> None:
        await self._consumer.start()
        try:
            async for msg in self._consumer:
                if msg is None:
                    continue

                if msg.topic == TopicKafkaEnum.COMPLETED_TASKS:
                    msg = self._deserialize_message(msg)
                    msg_dto = self._build_completed_task_dto(msg)
                    await self._service.process(msg_dto)

        finally:
            await self._consumer.stop()

    def _build_completed_task_dto(self, msg: dict[str, Any]) -> CompletedTaskDTO:
        return CompletedTaskDTO(**msg)

    def _deserialize_message(self, msg: ConsumerRecord) -> dict[str, Any]:
        logger.debug(
            f"Consumer: {self._name}, group_id: {self._group_id} received message from topic: "
            f"{msg.topic}, partition: {msg.partition}, offset: {msg.offset}, "
            f"key: {msg.key}, value: {msg.value.decode('utf-8')}"
        )
        return json.loads(msg.value.decode("utf-8"))


def get_completed_consumer(
    name: str,
    group_id: str,
    topics: list[str],
    service: AbstractHandlerServiceKafka,
) -> KafkaConsumer:
    return KafkaConsumer(name=name, group_id=group_id, topics=topics, service=service)
