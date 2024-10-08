import json
import logging
from dataclasses import asdict
from typing import Any

from confluent_kafka import Producer
from confluent_kafka.cimpl import KafkaException, Message

from apps.todo.infra.kafka.dto import CompletedTaskDTO
from apps.todo.infra.kafka.enums import TopicKafkaEnum
from config.todo.settings import KAFKA_CONFIG

logger = logging.getLogger("custom_logger")


class KafkaProducer:
    def __init__(self) -> None:
        self._producer = Producer(KAFKA_CONFIG)

    def send_completed_task(self, message: CompletedTaskDTO) -> None:
        valid_message = self._serialize_message(asdict(message))
        self._send_message(topic=TopicKafkaEnum.COMPLETED_TASKS, message=valid_message)

    def _serialize_message(self, data: dict[str, Any]) -> str:
        return json.dumps(data)

    def _send_message(self, topic: str, message: str) -> None:
        self._producer.produce(topic, value=message, callback=self._delivery_report)
        self._producer.flush()

    def _delivery_report(self, err: KafkaException, msg: Message) -> None:
        """Called once for each message produced to indicate delivery result. Triggered by poll() or flush()."""
        if err is not None:
            logger.error(f"Message delivery failed: {err}")
        else:
            logger.debug(
                f"Message {msg.value()} delivered to: \ntopic - {msg.topic()} \npartition - [{msg.partition()}]"
            )


def get_kafka_producer() -> KafkaProducer:
    return KafkaProducer()
