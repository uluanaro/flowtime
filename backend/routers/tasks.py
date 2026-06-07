from fastapi import APIRouter
from backend.models.database import get_db
from backend.models.schemas import CreateTask

router = APIRouter()

@router.get("/")
def get_tasks():
    conn = get_db()
    rows = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/")
def create_task(task: CreateTask):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO tasks (title, description, priority, due_date) VALUES (?, ?, ?, ?)",
        (task.title, task.description, task.priority, task.due_date)
    )
    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (new_id,)).fetchone()
    conn.commit()
    conn.close()
    return dict(row)

@router.patch("/{task_id}")
def update_task(task_id: int, updates: dict):
    conn = get_db()
    fields = ", ".join(f"{key} = ?" for key in updates.keys())
    values = list(updates.values()) + [task_id]
    conn.execute(
        f"UPDATE tasks SET {fields} WHERE id = ?", values
    )
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    conn.commit()
    conn.close()
    return dict(row)

@router.delete("/{task_id}")
def delete_task(task_id: int):
    conn = get_db()
    conn.execute(
        "DELETE FROM tasks WHERE id = ?",
        (task_id,))
    conn.commit()
    conn.close()
    return {"deleted": task_id}
