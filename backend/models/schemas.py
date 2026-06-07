from pydantic import BaseModel
from typing import Optional

class CreateTask(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    due_date: Optional[str] = None

class FixedEventCreate(BaseModel):
    title: str
    date: str
    start_time: str
    end_time: str