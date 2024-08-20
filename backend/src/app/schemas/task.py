from pydantic import BaseModel


class Task(BaseModel):
    id: str
    content: str
    is_completed: bool
    owner_id: str


class TaskResponse(BaseModel):
    id: str
    content: str
    is_completed: bool

    @classmethod
    def from_task(cls, task: Task) -> "TaskResponse":
        return cls(
            id=task.id,
            content=task.content,
            is_completed=task.is_completed
        )
