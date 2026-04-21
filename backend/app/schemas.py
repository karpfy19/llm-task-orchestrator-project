# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import uuid

class CreateTaskRequest(BaseModel):
    name: str
    prompt: str
    scheduled_at: Optional[datetime] = None
    parent_task_id: Optional[uuid.UUID] = None

class TaskResponse(BaseModel):
    id: uuid.UUID
    name: str
    prompt: str
    status: str
    scheduled_at: Optional[datetime]
    created_at: datetime
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    output: Optional[str]
    error: Optional[str]
    parent_task_id: Optional[uuid.UUID]

    class Config:
        orm_mode = True