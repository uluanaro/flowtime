from fastapi import APIRouter, HTTPException
from backend.services.ai_service import (
    estimate_task_duration,
    breakdown_goal,
    plan_day
)
from backend.models.database import get_db
from backend.routers.schedule import get_free_slots
from pydantic import BaseModel
from typing import Optional


router = APIRouter()

class EstimateRequest(BaseModel):
    title: str
    description: Optional[str] = None

class BreakdownRequest(BaseModel):
    title: str
    description: Optional[str] = None

class PlanDayRequest(BaseModel):
    date: str

@router.post("/estimate")
def estimate(request: EstimateRequest):
    try:
        result = estimate_task_duration(request.title, request.description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/breakdown")
def breakdown(task: BreakdownRequest):
    try:
        result = breakdown_goal(task.title, task.description)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/plan-day")
def plan_day_route(request: PlanDayRequest):
    conn = get_db()
    slots_data = get_free_slots(request.date)
    free_slots = slots_data["free_slots"]
    rows = conn.execute("SELECT * FROM tasks WHERE status = 'pending'").fetchall()
    tasks = [dict(row) for row in rows]
    conn.close()
    try:
        result = plan_day(free_slots=free_slots, tasks=tasks)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))