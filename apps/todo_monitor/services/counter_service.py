import logging

from apps.common.kafka.dto import CompletedTaskDTO

logger = logging.getLogger(__name__)


class CounterCompletedTaskHandlerService:

    def process(self, msg: CompletedTaskDTO) -> None:
        logger.debug(f"AAA {msg}")
