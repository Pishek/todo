from dataclasses import dataclass


@dataclass
class CompletedTaskDTO:
    user_id: int
    task_id: int
    title: str
    priority: str
    status: str
    created_at: str
    completed_at: str
    duration_in_days: int
