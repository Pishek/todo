from confluent_kafka import Producer

config = {
    'bootstrap.servers': 'kafka:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}


producer = Producer(config)

def send_message(topic, message):
    producer.produce(topic, value=message)
    producer.flush()