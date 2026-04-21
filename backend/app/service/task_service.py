# service.py
from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models import Task
from app.repository.task_repository import TaskRepository
from app.schemas import CreateTaskRequest
import uuid

class TaskService:

    def __init__(self):
        self.repo = TaskRepository()

    def create_task(self, db: Session, req: CreateTaskRequest) -> Task:
        scheduled_at = req.scheduled_at or datetime.now(timezone.utc)

        # Optional: validate parent task
        if req.parent_task_id:
            parent = self.repo.get_by_id(db, req.parent_task_id)
            if not parent:
                raise ValueError("Parent task not found")
            if parent.status != "COMPLETED":
                raise ValueError("Parent task must be completed")

        task = Task(
            name=req.name,
            prompt=req.prompt,
            status="PENDING",
            scheduled_at=scheduled_at,
            parent_task_id=req.parent_task_id
        )

        return self.repo.create(db, task)

    def list_tasks(self, db: Session):
        return self.repo.get_all(db)

    def get_task(self, db: Session, task_id: uuid.UUID):
        task = self.repo.get_by_id(db, task_id)
        if not task:
            raise ValueError("Task not found")
        return task