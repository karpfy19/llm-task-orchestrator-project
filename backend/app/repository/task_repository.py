# repository.py
from sqlalchemy.orm import Session
from app.models import Task
from typing import List, Optional
import uuid

class TaskRepository:

    def create(self, db: Session, task: Task) -> Task:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task

    def get_all(self, db: Session) -> List[Task]:
        return db.query(Task).order_by(Task.created_at.desc()).all()

    def get_by_id(self, db: Session, task_id: uuid.UUID) -> Optional[Task]:
        return db.query(Task).filter(Task.id == task_id).first()