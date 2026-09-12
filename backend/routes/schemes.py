from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/schemes",
    tags=["Government Schemes"]
)


SCHEMES = [
    {
        "id": 1,
        "name": "PM-KISAN",
        "category": "Income Support",
        "description": "Financial support scheme for eligible farmer families.",
        "eligibility": "Eligible farmer families as per government guidelines.",
        "documents": [
            "Aadhaar",
            "Bank account details",
            "Land-related documents"
        ],
        "application_mode": "Online / Government service centre",
        "official_source": "Government portal"
    },
    {
        "id": 2,
        "name": "Pradhan Mantri Fasal Bima Yojana",
        "category": "Crop Insurance",
        "description": "Crop insurance support against specified crop losses.",
        "eligibility": "Farmers growing notified crops in notified areas.",
        "documents": [
            "Aadhaar",
            "Bank account details",
            "Land or crop details"
        ],
        "application_mode": "Online / Bank / Common service centre",
        "official_source": "Government portal"
    },
    {
        "id": 3,
        "name": "Soil Health Card",
        "category": "Soil Health",
        "description": "Helps farmers understand soil nutrient status and fertilizer recommendations.",
        "eligibility": "Farmers seeking soil testing and nutrient guidance.",
        "documents": [
            "Basic farmer details",
            "Land or field details"
        ],
        "application_mode": "Agriculture department / Local service centre",
        "official_source": "Government agriculture department"
    }
]


@router.get("/")
def get_all_schemes():

    return {
        "status": "success",
        "total_schemes": len(SCHEMES),
        "schemes": SCHEMES,
        "note": (
            "Scheme rules, eligibility and application dates can change. "
            "Users should verify the latest information from the official government source."
        )
    }


@router.get("/{scheme_id}")
def get_scheme(scheme_id: int):

    for scheme in SCHEMES:
        if scheme["id"] == scheme_id:
            return {
                "status": "success",
                "scheme": scheme
            }

    raise HTTPException(
        status_code=404,
        detail="Scheme not found."
    )