import asyncio

from apps.todo_monitor.infra.kafka.consumer import get_completed_consumer
from apps.todo_monitor.logger import setup_logging


async def run_comleted_tasks_consumer() -> None:
    consumer = get_completed_consumer()
    await consumer.process_loop()


if __name__ == "__main__":
    setup_logging()
    asyncio.run(run_comleted_tasks_consumer())
