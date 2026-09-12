from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import sqlite3


router = APIRouter(
    prefix="/api/consultation",
    tags=["Consultation"]
)


DB_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "database"
    / "carebloom.db"
)


# ============================================================
# REQUEST MODELS
# ============================================================

class ConsultationRequest(BaseModel):
    user_id: int
    plant_id: int
    disease: str
    question: str


class ExpertReplyRequest(BaseModel):
    expert_name: str
    reply: str


class ConsultationStatusRequest(BaseModel):
    status: str


# ============================================================
# DATABASE TABLE
# ============================================================

def create_consultation_table():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS consultations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plant_id INTEGER NOT NULL,
            disease TEXT,
            question TEXT NOT NULL,
            expert_name TEXT,
            expert_reply TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            replied_at TIMESTAMP
        )
    """)

    # Handle older database that already has consultations table
    cursor.execute("PRAGMA table_info(consultations)")
    columns = [row[1] for row in cursor.fetchall()]

    if "expert_name" not in columns:
        cursor.execute("""
            ALTER TABLE consultations
            ADD COLUMN expert_name TEXT
        """)

    if "expert_reply" not in columns:
        cursor.execute("""
            ALTER TABLE consultations
            ADD COLUMN expert_reply TEXT
        """)

    if "replied_at" not in columns:
        cursor.execute("""
            ALTER TABLE consultations
            ADD COLUMN replied_at TIMESTAMP
        """)

    connection.commit()
    connection.close()


# ============================================================
# ADD CONSULTATION
# ============================================================

@router.post("/add")
def add_consultation(data: ConsultationRequest):

    try:

        create_consultation_table()

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

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
            "status": "success",
            "message": "Consultation request submitted",
            "consultation_id": consultation_id,
            "consultation_status": "Pending"
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to submit consultation: {str(error)}"
        )


# ============================================================
# GET USER CONSULTATIONS
# ============================================================

@router.get("/user/{user_id}")
def get_user_consultations(user_id: int):

    try:

        create_consultation_table()

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                user_id,
                plant_id,
                disease,
                question,
                expert_name,
                expert_reply,
                status,
                created_at,
                replied_at
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
                "expert_name": row[5],
                "expert_reply": row[6],
                "status": row[7],
                "created_at": row[8],
                "replied_at": row[9]
            })

        return {
            "status": "success",
            "user_id": user_id,
            "total_consultations": len(consultations),
            "consultations": consultations
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to load consultations: {str(error)}"
        )


# ============================================================
# GET ALL CONSULTATIONS FOR EXPERT
# ============================================================

@router.get("/expert/all")
def get_all_consultations():

    try:

        create_consultation_table()

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                user_id,
                plant_id,
                disease,
                question,
                expert_name,
                expert_reply,
                status,
                created_at,
                replied_at
            FROM consultations
            ORDER BY
                CASE
                    WHEN status = 'Pending' THEN 0
                    ELSE 1
                END,
                id DESC
        """)

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
                "expert_name": row[5],
                "expert_reply": row[6],
                "status": row[7],
                "created_at": row[8],
                "replied_at": row[9]
            })

        return {
            "status": "success",
            "total_consultations": len(consultations),
            "consultations": consultations
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to load expert consultations: {str(error)}"
        )


# ============================================================
# EXPERT REPLY
# ============================================================

@router.put("/{consultation_id}/reply")
def reply_to_consultation(
    consultation_id: int,
    data: ExpertReplyRequest
):

    if not data.reply.strip():
        raise HTTPException(
            status_code=400,
            detail="Expert reply cannot be empty."
        )

    try:

        create_consultation_table()

        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE consultations

            SET
                expert_name = ?,
                expert_reply = ?,
                status = 'Answered',
                replied_at = CURRENT_TIMESTAMP

            WHERE id = ?
        """, (
            data.expert_name.strip(),
            data.reply.strip(),
            consultation_id
        ))

        connection.commit()

        if cursor.rowcount == 0:

            connection.close()

            raise HTTPException(
                status_code=404,
                detail="Consultation not found."
            )

        connection.close()

        return {
            "status": "success",
            "consultation_id": consultation_id,
            "consultation_status": "Answered",
            "expert_name": data.expert_name,
            "reply": data.reply,
            "message": "Expert reply submitted successfully"
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to submit expert reply: {str(error)}"
        )


# ============================================================
# UPDATE STATUS
# ============================================================

@router.put("/{consultation_id}/status")
def update_consultation_status(
    consultation_id: int,
    data: ConsultationStatusRequest
):

    status = data.status.strip().title()

    valid_status = [
        "Pending",
        "In Progress",
        "Answered",
        "Closed"
    ]

    if status not in valid_status:

        raise HTTPException(
            status_code=400,
            detail=(
                "Status must be Pending, "
                "In Progress, Answered, or Closed."
            )
        )

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE consultations
        SET status = ?
        WHERE id = ?
    """, (
        status,
        consultation_id
    ))

    connection.commit()

    if cursor.rowcount == 0:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Consultation not found."
        )

    connection.close()

    return {
        "status": "success",
        "consultation_id": consultation_id,
        "consultation_status": status
    }


# ============================================================
# CONSULTATION SERVICE STATUS
# ============================================================

@router.get("/")
def consultation_service_status():

    return {
        "status": "running",
        "service": "CareBloom Expert Consultation Service"
    }