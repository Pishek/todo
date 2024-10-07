from confluent_kafka import Producer

from config.todo.settings import KAFKA_CONFIG

producer = Producer(KAFKA_CONFIG)


def send_message(topic, message):  # type: ignore
    producer.produce(topic, value=message)
    producer.flush()
