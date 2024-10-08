from dataclasses import dataclass
from datetime import datetime


@dataclass
class CompletedTaskDTO:
    user_id: int
    title: str
    priority: str
    created_at: datetime
    completed_at: datetime
