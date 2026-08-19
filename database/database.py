import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parent / "carebloom.db"


def create_tables():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Create disease history table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS disease_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            plant TEXT,
            disease TEXT,
            confidence REAL,
            health_score INTEGER,
            health_status TEXT,
            organic_remedy TEXT,
            chemical_treatment TEXT,
            prevention TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Safely add user_id column if it does not already exist
    cursor.execute("PRAGMA table_info(disease_history)")
    columns = [column[1] for column in cursor.fetchall()]

    if "user_id" not in columns:
        cursor.execute("""
            ALTER TABLE disease_history
            ADD COLUMN user_id INTEGER
        """)

    connection.commit()
    connection.close()


def save_disease_history(
    user_id,
    filename,
    plant,
    disease,
    confidence,
    health_score,
    health_status,
    organic_remedy,
    chemical_treatment,
    prevention
):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO disease_history (
            user_id,
            filename,
            plant,
            disease,
            confidence,
            health_score,
            health_status,
            organic_remedy,
            chemical_treatment,
            prevention
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        filename,
        plant,
        disease,
        confidence,
        health_score,
        health_status,
        organic_remedy,
        chemical_treatment,
        prevention
    ))

    connection.commit()
    connection.close()


def get_disease_history(user_id=None):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    if user_id is not None:
        cursor.execute("""
            SELECT
                id,
                user_id,
                filename,
                plant,
                disease,
                confidence,
                health_score,
                health_status,
                created_at
            FROM disease_history
            WHERE user_id = ?
            ORDER BY id DESC
        """, (user_id,))
    else:
        cursor.execute("""
            SELECT
                id,
                user_id,
                filename,
                plant,
                disease,
                confidence,
                health_score,
                health_status,
                created_at
            FROM disease_history
            ORDER BY id DESC
        """)

    rows = cursor.fetchall()
    connection.close()

    history = []

    for row in rows:
        history.append({
            "id": row[0],
            "user_id": row[1],
            "filename": row[2],
            "plant": row[3],
            "disease": row[4],
            "confidence": row[5],
            "health_score": row[6],
            "health_status": row[7],
            "created_at": row[8]
        })

    return history