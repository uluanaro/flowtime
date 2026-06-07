from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.models.database import init_db
from backend.routers import tasks, schedule, ai_planner
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title="flowtime", version="0.0.1", lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks.router, prefix="/api/tasks")
app.include_router(schedule.router, prefix="/api/schedule")
app.include_router(ai_planner.router, prefix="/api/ai")


@app.get("/health")
def health():
    return {"status": "ok",
            "app": "FlowTime",}

