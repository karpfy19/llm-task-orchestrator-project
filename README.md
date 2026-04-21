TASK SYSTEM (FASTAPI + NEXT.JS + POSTGRESQL + BACKGROUND WORKER)

This project is a full-stack task execution system built with:

- FastAPI (backend API)
- PostgreSQL (persistent storage)
- Next.js (frontend UI)
- Python background worker (asynchronous task execution)
- Docker Compose (full system orchestration)

------------------------------------------------------------

RUNNING THE PROJECT

Prerequisites:
- Docker Desktop installed and running

Start the system:

docker compose up --build

------------------------------------------------------------

ACCESS POINTS

Frontend:
http://localhost:3000

Backend API:
http://localhost:8000/docs

PostgreSQL:
localhost:5432

------------------------------------------------------------

SYSTEM OVERVIEW

This system allows users to create tasks that are executed asynchronously in the background.

Each task includes:
- name
- prompt (input to be processed)
- optional scheduled execution time
- lifecycle status tracking

------------------------------------------------------------

END-TO-END FEATURE FLOW

1. User creates a task via the frontend or API
2. FastAPI validates and stores the task in PostgreSQL
3. Task appears immediately with status PENDING
4. Background worker continuously polls the database
5. Worker executes eligible tasks asynchronously
6. Task transitions through states:
   PENDING → RUNNING → COMPLETED / FAILED
7. Frontend reflects updated state via API

This demonstrates a full vertical slice:
Frontend → Backend → Database → Background Processing

------------------------------------------------------------

BACKGROUND PROCESSING DESIGN

Execution Model:

The system uses a lightweight polling-based worker embedded within the FastAPI backend process.

Instead of using external infrastructure (Redis, Kafka, etc.), the worker:
- runs in a daemon thread
- continuously polls the database
- executes tasks sequentially

------------------------------------------------------------

WHY THIS APPROACH

This design was chosen for simplicity:

- No external infrastructure required
- Fully self-contained via Docker Compose
- Easy to reason about execution flow
- Simple debugging and predictable behavior

------------------------------------------------------------

TASK EXECUTION FLOW

1. Worker polls database at a fixed interval
2. Selects tasks where:
   - status = PENDING
   - scheduled_at is NULL OR <= current time
3. Marks task as RUNNING
4. Executes task using LLM client
5. Stores result in database
6. Marks task as COMPLETED or FAILED

------------------------------------------------------------

BACKEND INTEGRATION

The worker is tightly integrated with the backend:

- Shares SQLAlchemy session layer (SessionLocal)
- Uses repository pattern for all database access
- Started during FastAPI application startup
- Runs independently from API request lifecycle

This ensures:
- API remains stateless and responsive
- Background execution does not block requests
- Clear separation of concerns

------------------------------------------------------------

UX FLOW

The user experience is intentionally minimal:

- Users create tasks via a simple form
- Tasks are listed with real-time status updates
- No manual refresh required
- Optional scheduling via timestamp

Goal: clarity and predictability over UI complexity

------------------------------------------------------------

ARCHITECTURE

Backend (FastAPI):
- REST API for task creation and retrieval
- Service + repository pattern
- SQLAlchemy ORM

Worker:
- Background polling loop
- Sequential task execution
- Updates database state

Database (PostgreSQL):
- Stores all tasks
- Persistent Docker volume
- Auto-initialized on startup

Frontend (Next.js):
- Simple UI for task management
- Communicates via REST API
- Uses environment variable for backend URL

------------------------------------------------------------

DESIGN TRADEOFFS

Polling Worker:
+ Simple
+ No infrastructure dependencies
+ Easy debugging
- Less scalable
- Latency depends on polling interval

Queue-based systems (Celery / Redis / Kafka):
+ Scalable
+ Event-driven
+ Production-grade
- Requires extra infrastructure

------------------------------------------------------------

OPEN SOURCE ANALOGUES

This design is conceptually similar to:

- Celery (without broker)
- RQ (Redis Queue)
- Sidekiq (Ruby background jobs)

------------------------------------------------------------

ENVIRONMENT VARIABLES

Backend:
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/appdb

Frontend:
NEXT_PUBLIC_API_URL=http://backend:8000

------------------------------------------------------------

STOPPING THE SYSTEM

docker compose down

Reset database:
docker compose down -v

------------------------------------------------------------

MANUAL DEVELOPMENT (OPTIONAL)

Backend:
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

Frontend:
cd frontend
npm install
npm run dev

Requires local PostgreSQL setup.

------------------------------------------------------------

FUTURE IMPROVEMENTS

- Replace polling worker with queue-based system (Celery / Redis Queue)
- Add retry and backoff logic for failed tasks
- Support horizontal scaling of workers
- Add WebSocket-based real-time updates
- Improve observability (logging, metrics, tracing)

------------------------------------------------------------

TECH STACK

- FastAPI
- PostgreSQL
- SQLAlchemy
- Next.js
- Docker Compose
