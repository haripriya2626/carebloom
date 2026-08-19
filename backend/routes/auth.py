
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3
from pathlib import Path
import hashlib


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


DB_PATH = Path(__file__).resolve().parent.parent.parent / "database" / "carebloom.db"


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register_user(user: RegisterRequest):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    hashed_password = hashlib.sha256(
        user.password.encode()
    ).hexdigest()

    try:
        cursor.execute("""
            INSERT INTO users (
                name,
                email,
                password
            )
            VALUES (?, ?, ?)
        """, (
            user.name,
            user.email,
            hashed_password
        ))

        connection.commit()

    except sqlite3.IntegrityError:
        connection.close()

        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    user_id = cursor.lastrowid

    connection.close()

    return {
        "message": "User registered successfully",
        "user_id": user_id,
        "name": user.name,
        "email": user.email
    }
@router.post("/login")
def login_user(user: LoginRequest):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    hashed_password = hashlib.sha256(
        user.password.encode()
    ).hexdigest()

    cursor.execute("""
        SELECT id, name, email
        FROM users
        WHERE email = ? AND password = ?
    """, (
        user.email,
        hashed_password
    ))

    result = cursor.fetchone()

    connection.close()

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    return {
        "message": "Login successful",
        "user_id": result[0],
        "name": result[1],
        "email": result[2]
    }