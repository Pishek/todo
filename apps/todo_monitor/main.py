from typer import Typer

from apps.common.kafka.enums import TopicKafkaEnum
from apps.todo_monitor.infra.kafka.consumer import get_completed_consumer
from apps.todo_monitor.logger import setup_logging
from apps.todo_monitor.services.counter_service import get_counter_service
from apps.todo_monitor.services.task_info_service import get_task_info_service
from apps.todo_monitor.utils import coro

app = Typer()


@app.command(help="Запуск консьюмера по подсчету завершенных задач.")
@coro
async def run_comleted_tasks_consumer(name: str, group_id: str) -> None:
    setup_logging()
    service = get_counter_service()
    consumer = get_completed_consumer(
        name=name,
        group_id=group_id,
        topics=[TopicKafkaEnum.COMPLETED_TASKS],
        service=service,
    )
    await consumer.process_loop()


@app.command(help="Запуск консьюмера по сохранению информации о завершенных задачах.")
@coro
async def run_info_tasks_consumer(name: str, group_id: str) -> None:
    setup_logging()
    service = get_task_info_service()
    consumer = get_completed_consumer(
        name=name,
        group_id=group_id,
        topics=[TopicKafkaEnum.COMPLETED_TASKS],
        service=service,
    )
    await consumer.process_loop()


if __name__ == "__main__":
    app()
