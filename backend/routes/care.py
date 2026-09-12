from fastapi import APIRouter, HTTPException

from backend.services.disease_care import get_disease_care


# ============================================================
# CARE ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/care",
    tags=["Plant Care"]
)


# ============================================================
# GET DISEASE CARE DETAILS
# ============================================================

@router.get("/{disease}")
def get_care_details(
    disease: str,
    confidence: float = 0
):
    """
    Returns plant disease care information including:

    - Disease description
    - Symptoms
    - Organic remedies
    - Treatment
    - Prevention
    - Plant health score
    """

    try:

        # Validate confidence
        if confidence < 0 or confidence > 100:
            raise HTTPException(
                status_code=400,
                detail="Confidence must be between 0 and 100."
            )

        care_data = get_disease_care(
            disease=disease,
            confidence=confidence
        )

        return {
            "status": "success",
            "data": care_data
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to get plant care information: {str(error)}"
        )


# ============================================================
# CARE API HEALTH CHECK
# ============================================================

@router.get("/")
def care_service_status():

    return {
        "status": "running",
        "service": "CareBloom Plant Care Engine",
        "message": "Plant care service is available."
    }