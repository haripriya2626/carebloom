from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
import sqlite3


router = APIRouter(
    prefix="/api/community",
    tags=["Farmer Community"]
)


DB_PATH = (
    Path(__file__).resolve().parent.parent.parent
    / "database"
    / "carebloom.db"
)


# ============================================================
# REQUEST MODELS
# ============================================================

class PostRequest(BaseModel):
    user_id: int
    title: str
    content: str


class CommentRequest(BaseModel):
    user_id: int
    comment: str


# ============================================================
# CREATE TABLES
# ============================================================

def create_community_tables():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            likes INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            comment TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# CREATE POST
# ============================================================

@router.post("/posts")
def create_post(data: PostRequest):

    if not data.title.strip():
        raise HTTPException(
            status_code=400,
            detail="Post title cannot be empty."
        )

    if not data.content.strip():
        raise HTTPException(
            status_code=400,
            detail="Post content cannot be empty."
        )

    create_community_tables()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO community_posts (
            user_id,
            title,
            content
        )
        VALUES (?, ?, ?)
    """, (
        data.user_id,
        data.title.strip(),
        data.content.strip()
    ))

    connection.commit()

    post_id = cursor.lastrowid

    connection.close()

    return {
        "status": "success",
        "message": "Community post created successfully",
        "post_id": post_id
    }


# ============================================================
# GET ALL POSTS
# ============================================================

@router.get("/posts")
def get_posts():

    create_community_tables()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            title,
            content,
            likes,
            created_at
        FROM community_posts
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    posts = []

    for row in rows:

        cursor.execute("""
            SELECT COUNT(*)
            FROM community_comments
            WHERE post_id = ?
        """, (row[0],))

        comment_count = cursor.fetchone()[0]

        posts.append({
            "post_id": row[0],
            "user_id": row[1],
            "title": row[2],
            "content": row[3],
            "likes": row[4],
            "comments": comment_count,
            "created_at": row[5]
        })

    connection.close()

    return {
        "status": "success",
        "total_posts": len(posts),
        "posts": posts
    }


# ============================================================
# GET ONE POST + COMMENTS
# ============================================================

@router.get("/posts/{post_id}")
def get_post(post_id: int):

    create_community_tables()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            user_id,
            title,
            content,
            likes,
            created_at
        FROM community_posts
        WHERE id = ?
    """, (post_id,))

    post = cursor.fetchone()

    if post is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Community post not found."
        )

    cursor.execute("""
        SELECT
            id,
            user_id,
            comment,
            created_at
        FROM community_comments
        WHERE post_id = ?
        ORDER BY id ASC
    """, (post_id,))

    comment_rows = cursor.fetchall()

    connection.close()

    comments = []

    for row in comment_rows:

        comments.append({
            "comment_id": row[0],
            "user_id": row[1],
            "comment": row[2],
            "created_at": row[3]
        })

    return {
        "status": "success",
        "post": {
            "post_id": post[0],
            "user_id": post[1],
            "title": post[2],
            "content": post[3],
            "likes": post[4],
            "created_at": post[5],
            "comments": comments
        }
    }


# ============================================================
# ADD COMMENT
# ============================================================

@router.post("/posts/{post_id}/comments")
def add_comment(
    post_id: int,
    data: CommentRequest
):

    if not data.comment.strip():

        raise HTTPException(
            status_code=400,
            detail="Comment cannot be empty."
        )

    create_community_tables()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id FROM community_posts WHERE id = ?",
        (post_id,)
    )

    if cursor.fetchone() is None:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Community post not found."
        )

    cursor.execute("""
        INSERT INTO community_comments (
            post_id,
            user_id,
            comment
        )
        VALUES (?, ?, ?)
    """, (
        post_id,
        data.user_id,
        data.comment.strip()
    ))

    connection.commit()

    comment_id = cursor.lastrowid

    connection.close()

    return {
        "status": "success",
        "message": "Comment added successfully",
        "comment_id": comment_id,
        "post_id": post_id
    }


# ============================================================
# LIKE POST
# ============================================================

@router.post("/posts/{post_id}/like")
def like_post(post_id: int):

    create_community_tables()

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE community_posts
        SET likes = likes + 1
        WHERE id = ?
    """, (post_id,))

    connection.commit()

    if cursor.rowcount == 0:

        connection.close()

        raise HTTPException(
            status_code=404,
            detail="Community post not found."
        )

    cursor.execute(
        "SELECT likes FROM community_posts WHERE id = ?",
        (post_id,)
    )

    likes = cursor.fetchone()[0]

    connection.close()

    return {
        "status": "success",
        "post_id": post_id,
        "likes": likes,
        "message": "Post liked successfully"
    }


# ============================================================
# SERVICE STATUS
# ============================================================

@router.get("/")
def community_service_status():

    return {
        "status": "running",
        "service": "CareBloom Farmer Community"
    }
