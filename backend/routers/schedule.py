from typing import List

from fastapi import APIRouter
from backend.models.database import get_db
from backend.models.schemas import FixedEventCreate

router = APIRouter()

@router.get("/events", response_model=List[FixedEventCreate])
def get_schedule(date: str = None):
    conn = get_db()
    if date:
        rows = conn.execute("SELECT * FROM fixed_events WHERE date = ?", (date,)).fetchall()
    else:
        rows = conn.execute("SELECT * FROM fixed_events").fetchall()
    conn.close()
    return [dict(row) for row in rows]

@router.post("/events", response_model=FixedEventCreate)
def create_schedule(event: FixedEventCreate):
    conn = get_db()
    cursor = conn.execute(
        "INSERT INTO fixed_events (title, date, start_time, end_time) VALUES (?, ?, ?, ?)",
        (event.title, event.date, event.start_time, event.end_time)
    )
    new_id = cursor.lastrowid
    row = conn.execute("SELECT * FROM fixed_events WHERE id = ?", (new_id,)).fetchone()
    conn.commit()
    conn.close()
    return dict(row)

@router.delete("/events/{event_id}")
def delete_event(event_id: int):
    conn = get_db()
    conn.execute("DELETE FROM fixed_events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()
    return {"deleted": event_id}



def to_minutes(time_str: str) -> int:
    # "09:30" → 570
    # подсказка: split(":") даст ["09", "30"]
    hours = int(time_str.split(":")[0]) * 60
    minutes = int(time_str.split(":")[1])
    return hours + minutes


def from_minutes(minutes: int) -> str:
    # 570 → "09:30"
    # подсказка: // и % операторы
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02d}:{minutes:02}"


@router.get("/free-slots/{date}")
def get_free_slots(date: str):
    # 1. получи события дня из БД, отсортируй по start_time
    # 2. примени алгоритм выше
    # 3. верни {"date": date, "free_slots": [...], "total_free_minutes": ...}
    conn = get_db()
    events = conn.execute("SELECT start_time, end_time FROM fixed_events WHERE date = ? ORDER BY start_time", (date,)
    ).fetchall()
    conn.close()

    day_start = to_minutes("08:00")
    day_end = to_minutes("22:00")
    cursor_pos = day_start
    free_slots = []

    for event in events:
        event_start = to_minutes(event["start_time"])
        event_end = to_minutes(event["end_time"])
        # print(f"cursor_pos={from_minutes(cursor_pos)}, event_start={from_minutes(event_start)}")
        if event_start > cursor_pos:
            free_slots.append({
                "start": from_minutes(cursor_pos),
                "end": from_minutes(event_start),
                "minutes": event_start - cursor_pos
            })
        cursor_pos = event_end

    if day_end > cursor_pos:
        # print(f"FINAL cursor_pos={from_minutes(cursor_pos)}")
        free_slots.append({
            "start": from_minutes(cursor_pos),
            "end": from_minutes(day_end),
            "minutes": day_end - cursor_pos
        })

    return {
        "date": date,
        "free_slots": free_slots,
        "total_free_minutes": sum(s["minutes"] for s in free_slots)
    }

