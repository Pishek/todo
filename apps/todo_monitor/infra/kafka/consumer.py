import json
import logging
from typing import Any

from confluent_kafka import Consumer, KafkaError, KafkaException, Message

from apps.common.kafka.dto import CompletedTaskDTO
from apps.todo_monitor.infra.kafka.enums import TopicKafkaEnum
from apps.todo_monitor.services.counter_service import CounterCompletedTaskHandlerService
from config.todo_monitor.settings import KAFKA_CONSUMER_CONFIG

logger = logging.getLogger(__name__)


class KafkaConsumer:
    def __init__(self, topics: list[str]) -> None:
        self._topics = topics
        self._consumer = Consumer(KAFKA_CONSUMER_CONFIG)
        self._counter_service = CounterCompletedTaskHandlerService()

    def process_loop(self) -> None:
        try:
            self._consumer.subscribe(self._topics)

            while True:
                msg = self._consumer.poll(timeout=1.0)
                if msg is None:
                    continue
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # Информационное сообщение о конце партиции
                        logger.debug(f"End of partition {msg.topic()} [{msg.partition()}] at offset {msg.offset()}")
                    elif msg.error():
                        raise KafkaException(msg.error())
                topic = msg.topic()
                self._consumer.commit(asynchronous=False)
                msg = self._deserialize_message(msg)

                if topic == TopicKafkaEnum.COMPLETED_TASKS:
                    msg_dto = self._build_completed_task_dto(msg)
                    self._counter_service.process(msg_dto)

        finally:
            self._consumer.close()

    def _build_completed_task_dto(self, msg: dict[str, Any]) -> CompletedTaskDTO:
        return CompletedTaskDTO(**msg)

    def _deserialize_message(self, msg: Message) -> dict[str, Any]:
        logger.debug(
            f"Received message from topic: {msg.topic()}, partition: {msg.partition()}, "
            f"offset: {msg.offset()}, key: {msg.key()}, value: {msg.value().decode('utf-8')}"
        )
        return json.loads(msg.value().decode("utf-8"))


def get_completed_consumer() -> KafkaConsumer:
    return KafkaConsumer(topics=[TopicKafkaEnum.COMPLETED_TASKS])
