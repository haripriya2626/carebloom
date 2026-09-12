from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from pwdlib import PasswordHash
import sqlite3
import hashlib


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


DB_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "database"
    / "carebloom.db"
)


# ============================================================
# PASSWORD HASHER
# ============================================================

password_hash = PasswordHash.recommended()


# ============================================================
# REQUEST MODELS
# ============================================================

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


# ============================================================
# OLD SHA-256 SUPPORT
# ============================================================

def verify_old_sha256(password: str, stored_hash: str) -> bool:
    old_hash = hashlib.sha256(
        password.encode()
    ).hexdigest()

    return old_hash == stored_hash


def is_old_sha256_hash(stored_hash: str) -> bool:
    return (
        len(stored_hash) == 64
        and all(
            char in "0123456789abcdef"
            for char in stored_hash.lower()
        )
    )


# ============================================================
# REGISTER
# ============================================================

@router.post("/register")
def register_user(user: RegisterRequest):

    name = user.name.strip()
    email = user.email.strip().lower()
    password = user.password

    # -----------------------------
    # Validation
    # -----------------------------

    if not name:
        raise HTTPException(
            status_code=400,
            detail="Name is required."
        )

    if not email:
        raise HTTPException(
            status_code=400,
            detail="Email is required."
        )

    if "@" not in email:
        raise HTTPException(
            status_code=400,
            detail="Please enter a valid email address."
        )

    if len(password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must contain at least 8 characters."
        )

    # Argon2 password hashing
    hashed_password = password_hash.hash(
        password
    )

    connection = sqlite3.connect(DB_PATH)

    try:
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

        cursor.execute("""
            INSERT INTO users (
                name,
                email,
                password
            )
            VALUES (?, ?, ?)
        """, (
            name,
            email,
            hashed_password
        ))

        connection.commit()

        user_id = cursor.lastrowid

    except sqlite3.IntegrityError:

        raise HTTPException(
            status_code=400,
            detail="Email already registered."
        )

    finally:
        connection.close()

    return {
        "status": "success",
        "message": "User registered successfully",
        "user_id": user_id,
        "name": name,
        "email": email
    }


# ============================================================
# LOGIN
# ============================================================

@router.post("/login")
def login_user(user: LoginRequest):

    email = user.email.strip().lower()
    password = user.password

    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT
                id,
                name,
                email,
                password
            FROM users
            WHERE LOWER(email) = ?
        """, (email,))

        result = cursor.fetchone()

        if not result:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password."
            )

        user_id = result[0]
        name = result[1]
        stored_email = result[2]
        stored_password = result[3]

        password_valid = False
        needs_upgrade = False

        # ------------------------------------
        # Existing SHA-256 account
        # ------------------------------------

        if is_old_sha256_hash(stored_password):

            password_valid = verify_old_sha256(
                password,
                stored_password
            )

            if password_valid:
                needs_upgrade = True

        # ------------------------------------
        # New Argon2 account
        # ------------------------------------

        else:
            try:
                password_valid = password_hash.verify(
                    password,
                    stored_password
                )

            except Exception:
                password_valid = False

        if not password_valid:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password."
            )

        # ------------------------------------
        # Automatically upgrade old password
        # ------------------------------------

        if needs_upgrade:

            new_hash = password_hash.hash(
                password
            )

            cursor.execute("""
                UPDATE users
                SET password = ?
                WHERE id = ?
            """, (
                new_hash,
                user_id
            ))

            connection.commit()

    finally:
        connection.close()

    return {
        "status": "success",
        "message": "Login successful",
        "user_id": user_id,
        "name": name,
        "email": stored_email
    }