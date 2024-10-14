from abc import ABC, abstractmethod

from apps.common.kafka.dto import CompletedTaskDTO


class AbstractHandlerServiceKafka(ABC):
    @abstractmethod
    async def process(self, data: CompletedTaskDTO) -> None: ...  # noqa E704
