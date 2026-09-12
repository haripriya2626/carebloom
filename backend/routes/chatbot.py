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
# VOICE LANGUAGE MAPPING
# Browser Speech Recognition / Speech Synthesis language codes
# ============================================================

VOICE_LANGUAGE_CODES = {
    "en": "en-IN",
    "ta": "ta-IN",
    "hi": "hi-IN",
    "te": "te-IN",
    "ml": "ml-IN",
    "kn": "kn-IN",
    "bn": "bn-IN",
    "mr": "mr-IN",
    "gu": "gu-IN",
    "pa": "pa-IN"
}


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
        "voice_language": VOICE_LANGUAGE_CODES.get(
            language,
            "en-IN"
        ),
        "user_message": message,
        "detected_topic": result["topic"],
        "reply": result["reply"],
        "engine": "CareBloom Multilingual Plant Assistant",
        "voice_enabled": True
    }


# ============================================================
# VOICE CONFIGURATION
# ============================================================

@router.get("/voice-config")
def voice_configuration():

    return {
        "status": "success",
        "voice_input": "Browser Speech Recognition",
        "voice_output": "Browser Speech Synthesis",
        "supported_languages": VOICE_LANGUAGE_CODES,
        "note": (
            "Speech-to-text and text-to-speech are handled "
            "by the CareBloom frontend using browser voice APIs."
        )
    }


# ============================================================
# CHATBOT STATUS
# ============================================================

@router.get("/")
def chatbot_status():

    return {
        "status": "running",
        "service": "CareBloom Multilingual AI Plant Chatbot",
        "supported_languages": len(VOICE_LANGUAGE_CODES),
        "text_chat": True,
        "voice_chat": True
    }