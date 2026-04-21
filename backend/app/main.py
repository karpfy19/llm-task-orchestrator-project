from contextlib import asynccontextmanager
import threading

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.tasks import router as tasks_router
from app.db.database import init_db
from app.worker.worker import TaskWorker


# -------------------------
# Worker bootstrap
# -------------------------
def start_worker():
    print("🚀 Worker starting...")
    TaskWorker().run_forever()


# -------------------------
# Lifespan (startup/shutdown)
# -------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔥 startup
    print("🔥 Initializing database...")
    init_db()

    print("🚀 Starting background worker...")
    thread = threading.Thread(target=start_worker, daemon=True)
    thread.start()

    yield

    # 🔥 shutdown
    print("👋 Shutting down...")


# -------------------------
# App setup
# -------------------------
app = FastAPI(lifespan=lifespan)

# -------------------------
# CORS
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Routes
# -------------------------
app.include_router(tasks_router)