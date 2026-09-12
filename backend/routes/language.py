from fastapi import APIRouter, HTTPException

from backend.services.language_service import (
    get_supported_languages,
    translate,
    is_supported_language,
    get_language_info
)


router = APIRouter(
    prefix="/api/language",
    tags=["Language Support"]
)


@router.get("/supported")
def supported_languages():

    return {
        "status": "success",
        "total_languages": len(get_supported_languages()),
        "languages": get_supported_languages()
    }


@router.get("/translate")
def translate_message(
    key: str,
    language: str = "en"
):

    if not is_supported_language(language):
        raise HTTPException(
            status_code=400,
            detail="Unsupported language code."
        )

    return {
        "status": "success",
        "language": get_language_info(language),
        "key": key,
        "translated_text": translate(
            key,
            language
        )
    }


@router.get("/")
def language_service_status():

    return {
        "status": "running",
        "service": "CareBloom Multilingual Language Service"
    }