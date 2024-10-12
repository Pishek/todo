from apps.todo_monitor.infra.kafka.consumer import get_completed_consumer
from config.todo_monitor.settings import setup_logging


def run_comleted_tasks_consumer() -> None:
    consumer = get_completed_consumer()
    consumer.process_loop()


if __name__ == "__main__":
    setup_logging()
    run_comleted_tasks_consumer()
