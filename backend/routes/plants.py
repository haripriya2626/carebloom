from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import sqlite3


router = APIRouter(
    prefix="/api/plants",
    tags=["Plants"]
)


DB_PATH = Path(__file__).resolve().parent.parent.parent / "database" / "carebloom.db"


class PlantRequest(BaseModel):
    user_id: int
    plant_name: str
    planting_date: str
    location: str


@router.post("/add")
def add_plant(plant: PlantRequest):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_plants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            plant_name TEXT NOT NULL,
            planting_date TEXT,
            location TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        INSERT INTO user_plants (
            user_id,
            plant_name,
            planting_date,
            location
        )
        VALUES (?, ?, ?, ?)
    """, (
        plant.user_id,
        plant.plant_name,
        plant.planting_date,
        plant.location
    ))

    connection.commit()

    plant_id = cursor.lastrowid

    connection.close()

    return {
        "message": "Plant added successfully",
        "plant_id": plant_id,
        "user_id": plant.user_id,
        "plant_name": plant.plant_name,
        "planting_date": plant.planting_date,
        "location": plant.location
    }
@router.get("/user/{user_id}")
def get_user_plants(user_id: int):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            plant_name,
            planting_date,
            location,
            created_at
        FROM user_plants
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    rows = cursor.fetchall()
    connection.close()

    plants = []

    for row in rows:
        plants.append({
            "plant_id": row[0],
            "user_id": row[1],
            "plant_name": row[2],
            "planting_date": row[3],
            "location": row[4],
            "created_at": row[5]
        })

    return plants