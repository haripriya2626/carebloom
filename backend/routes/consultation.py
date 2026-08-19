from fastapi import APIRouter
from pydantic import BaseModel
from pathlib import Path
import sqlite3


router = APIRouter(
    prefix="/api/consultation",
    tags=["Consultation"]
)


DB_PATH = Path(__file__).resolve().parent.parent.parent / "database" / "carebloom.db"


class ConsultationRequest(BaseModel):
    user_id: int
    plant_id: int
    disease: str
    question: str


@router.post("/add")
def add_consultation(data: ConsultationRequest):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plant_id INTEGER NOT NULL,
            disease TEXT,
            question TEXT NOT NULL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO consultations (
            user_id,
            plant_id,
            disease,
            question
        )
        VALUES (?, ?, ?, ?)
    """, (
        data.user_id,
        data.plant_id,
        data.disease,
        data.question
    ))

    connection.commit()
    consultation_id = cursor.lastrowid
    connection.close()

    return {
        "message": "Consultation request submitted",
        "consultation_id": consultation_id,
        "status": "Pending"
    }


@router.get("/user/{user_id}")
def get_user_consultations(user_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            plant_id,
            disease,
            question,
            status,
            created_at
        FROM consultations
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()
    connection.close()

    consultations = []

    for row in rows:
        consultations.append({
            "consultation_id": row[0],
            "user_id": row[1],
            "plant_id": row[2],
            "disease": row[3],
            "question": row[4],
            "status": row[5],
            "created_at": row[6]
        })

    return consultations