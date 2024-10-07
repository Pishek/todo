import json
from typing import Any

from confluent_kafka import Producer

from apps.todo.infra.kafka.enums import TopicKafkaEnum
from config.todo.settings import KAFKA_CONFIG


class KafkaProducer:
    def __init__(self) -> None:
        self._producer = Producer(KAFKA_CONFIG)

    def send_completed_task(self, message: dict[str, Any]) -> None:
        self.__send_message(topic=TopicKafkaEnum.COMPLETED_TASKS, message=message)

    def __send_message(self, topic: str, message: dict[str, Any]) -> None:
        self._producer.produce(topic, value=json.dumps(message))
        self._producer.flush()


def get_kafka_producer() -> KafkaProducer:
    return KafkaProducer()
