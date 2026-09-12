from backend.services.care_scheduler import get_care_schedule
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import sqlite3


router = APIRouter(
    prefix="/api/reminders",
    tags=["Reminders"]
)


DB_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "database"
    / "carebloom.db"
)


# ============================================================
# REQUEST MODELS
# ============================================================

class ReminderRequest(BaseModel):
    user_id: int
    plant_id: int
    reminder_type: str
    reminder_date: str
    message: str = ""

class AutoScheduleRequest(BaseModel):
    user_id: int
    plant_id: int
    plant_name: str
    rainfall: float = 0
    humidity: float = 0


class ReminderStatusRequest(BaseModel):
    status: str


# ============================================================
# DATABASE HELPER
# ============================================================

def create_reminder_table():

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

    connection.commit()
    connection.close()


# ============================================================
# ADD REMINDER
# ============================================================

@router.post("/add")
def add_reminder(reminder: ReminderRequest):

    try:

        create_reminder_table()

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

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
            "status": "success",
            "message": "Reminder added successfully",
            "reminder_id": reminder_id,
            "user_id": reminder.user_id,
            "plant_id": reminder.plant_id,
            "reminder_type": reminder.reminder_type,
            "reminder_date": reminder.reminder_date,
            "reminder_status": "Pending"
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to add reminder: {str(error)}"
        )


# ============================================================
# GET USER REMINDERS
# ============================================================

@router.get("/user/{user_id}")
def get_user_reminders(user_id: int):

    try:

        create_reminder_table()

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

        return {
            "status": "success",
            "user_id": user_id,
            "total_reminders": len(reminders),
            "reminders": reminders
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to load reminders: {str(error)}"
        )


# ============================================================
# UPDATE REMINDER STATUS
# ============================================================

@router.put("/{reminder_id}/status")
def update_reminder_status(
    reminder_id: int,
    request: ReminderStatusRequest
):

    valid_status = [
        "Pending",
        "Completed",
        "Cancelled"
    ]

    status = request.status.strip().title()

    if status not in valid_status:

        raise HTTPException(
            status_code=400,
            detail="Status must be Pending, Completed, or Cancelled."
        )

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        UPDATE reminders
        SET status = ?
        WHERE id = ?
    """, (
        status,
        reminder_id
    ))

    connection.commit()

    if cursor.rowcount == 0:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Reminder not found."
        )

    connection.close()

    return {
        "status": "success",
        "reminder_id": reminder_id,
        "reminder_status": status,
        "message": "Reminder status updated successfully"
    }


# ============================================================
# DELETE REMINDER
# ============================================================

@router.delete("/{reminder_id}")
def delete_reminder(reminder_id: int):

    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM reminders
        WHERE id = ?
    """, (reminder_id,))

    connection.commit()

    if cursor.rowcount == 0:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Reminder not found."
        )

    connection.close()

    return {
        "status": "success",
        "message": "Reminder deleted successfully",
        "reminder_id": reminder_id
    }
@router.post("/auto-schedule")
def auto_schedule_reminders(request: AutoScheduleRequest):

    try:

        create_reminder_table()

        schedule = get_care_schedule(
            plant=request.plant_name,
            rainfall=request.rainfall,
            humidity=request.humidity
        )

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        # Watering reminder
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
            request.user_id,
            request.plant_id,
            "Watering",
            schedule["next_watering_date"],
            f"Time to water your {request.plant_name} plant."
        ))

        watering_reminder_id = cursor.lastrowid

        # Fertilizer reminder
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
            request.user_id,
            request.plant_id,
            "Fertilizer",
            schedule["next_fertilizer_date"],
            f"Time to fertilize your {request.plant_name} plant."
        ))

        fertilizer_reminder_id = cursor.lastrowid

        connection.commit()
        connection.close()

        return {
            "status": "success",
            "message": "Automatic care reminders created",
            "plant": request.plant_name,
            "watering": {
                "reminder_id": watering_reminder_id,
                "date": schedule["next_watering_date"],
                "interval_days": schedule["watering_interval_days"]
            },
            "fertilizer": {
                "reminder_id": fertilizer_reminder_id,
                "date": schedule["next_fertilizer_date"],
                "interval_days": schedule["fertilizer_interval_days"]
            },
            "weather_adjusted": schedule["weather_adjusted"],
            "note": schedule["note"]
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to create automatic reminders: {str(error)}"
        )


# ============================================================
# SERVICE STATUS
# ============================================================

@router.get("/")
def reminder_service_status():

    return {
        "status": "running",
        "service": "CareBloom Reminder Service"
    }