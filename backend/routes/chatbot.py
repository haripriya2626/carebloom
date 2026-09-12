from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.language_service import (
    is_supported_language
)

from backend.services.chatbot_service import (
    generate_chatbot_reply
)


router = APIRouter(
    prefix="/api/chatbot",
    tags=["AI Plant Chatbot"]
)


# ============================================================
# REQUEST MODEL
# ============================================================

class ChatRequest(BaseModel):
    message: str
    language: str = "en"


# ============================================================
# ASK CHATBOT
# ============================================================

@router.post("/ask")
def ask_chatbot(data: ChatRequest):

    message = data.message.strip()
    language = data.language.strip().lower()

    if not message:
        raise HTTPException(
            status_code=400,
            detail="Please enter a question."
        )

    if not is_supported_language(language):
        raise HTTPException(
            status_code=400,
            detail="Unsupported language code."
        )

    result = generate_chatbot_reply(
        message=message,
        language=language
    )

    return {
        "status": "success",
        "language": result["language"],
        "user_message": message,
        "detected_topic": result["topic"],
        "reply": result["reply"],
        "engine": "CareBloom Multilingual Plant Assistant"
    }


# ============================================================
# CHATBOT STATUS
# ============================================================

@router.get("/")
def chatbot_status():

    return {
        "status": "running",
        "service": "CareBloom Multilingual AI Plant Chatbot",
        "supported_languages": 10
    }