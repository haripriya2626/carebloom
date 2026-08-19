from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import sqlite3


router = APIRouter(
    prefix="/api/reminders",
    tags=["Reminders"]
)


DB_PATH = Path(__file__).resolve().parent.parent.parent / "database" / "carebloom.db"


class ReminderRequest(BaseModel):
    user_id: int
    plant_id: int
    reminder_type: str
    reminder_date: str
    message: str


@router.post("/add")
def add_reminder(reminder: ReminderRequest):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plant_id INTEGER NOT NULL,
            reminder_type TEXT NOT NULL,
            reminder_date TEXT NOT NULL,
            message TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO reminders (
            user_id,
            plant_id,
            reminder_type,
            reminder_date,
            message
        )
        VALUES (?, ?, ?, ?, ?)
    """, (
        reminder.user_id,
        reminder.plant_id,
        reminder.reminder_type,
        reminder.reminder_date,
        reminder.message
    ))

    connection.commit()

    reminder_id = cursor.lastrowid
    connection.close()

    return {
        "message": "Reminder added successfully",
        "reminder_id": reminder_id,
        "user_id": reminder.user_id,
        "plant_id": reminder.plant_id,
        "reminder_type": reminder.reminder_type,
        "reminder_date": reminder.reminder_date,
        "status": "Pending"
    }


@router.get("/user/{user_id}")
def get_user_reminders(user_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            plant_id,
            reminder_type,
            reminder_date,
            message,
            status,
            created_at
        FROM reminders
        WHERE user_id = ?
        ORDER BY reminder_date ASC
    """, (user_id,))

    rows = cursor.fetchall()
    connection.close()

    reminders = []

    for row in rows:
        reminders.append({
            "reminder_id": row[0],
            "user_id": row[1],
            "plant_id": row[2],
            "reminder_type": row[3],
            "reminder_date": row[4],
            "message": row[5],
            "status": row[6],
            "created_at": row[7]
        })

    return reminders