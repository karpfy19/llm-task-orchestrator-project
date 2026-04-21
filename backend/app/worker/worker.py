import time
from datetime import datetime, timezone

from app.db.database import SessionLocal
from app.repository.task_repository import TaskRepository
from app.llm.client import LLMClient


POLL_INTERVAL = 2  # seconds


class TaskWorker:
    def __init__(self):
        self.repo = TaskRepository()
        self.llm = LLMClient()

    def run_forever(self):
        print("Worker started...")

        while True:
            db = SessionLocal()

            try:
                task = self.fetch_next_task(db)

                if task:
                    self.execute_task(db, task)

            except Exception as e:
                print(f"Worker error: {e}")

            finally:
                db.close()

            time.sleep(POLL_INTERVAL)

    # -------------------------
    # Fetch next runnable task
    # -------------------------
    def fetch_next_task(self, db):
        tasks = self.repo.get_all(db)

        for task in tasks:
            if task.status == "PENDING":
                if task.scheduled_at is None or task.scheduled_at <= datetime.now(timezone.utc):
                    return task

        return None

    # -------------------------
    # Mark running
    # -------------------------
    def mark_running(self, db, task):
        task.status = "RUNNING"
        db.commit()

    # -------------------------
    # Execute task
    # -------------------------
    def execute_task(self, db, task):
        try:
            self.mark_running(db, task)

            result = self.llm.run(task.prompt)

            task.output = result
            task.status = "COMPLETED"
            task.completed_at = datetime.now(timezone.utc)

            db.commit()

        except Exception as e:
            task.status = "FAILED"
            task.error = str(e)

            db.commit()