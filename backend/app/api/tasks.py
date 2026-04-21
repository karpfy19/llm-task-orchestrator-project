# api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.schemas import CreateTaskRequest, TaskResponse
from app.service.task_service import TaskService
from app.db.database import get_db

router = APIRouter()
service = TaskService()

@router.post("/tasks", response_model=TaskResponse)
def create_task(req: CreateTaskRequest, db: Session = Depends(get_db)):
    try:
        task = service.create_task(db, req)
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/tasks", response_model=List[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    print("🔥 ENDPOINT HIT")
    print("DB =", db)
    return service.list_tasks(db)


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: uuid.UUID, db: Session = Depends(get_db)):
    try:
        return service.get_task(db, task_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))