from fastapi import APIRouter, HTTPException

router = APIRouter(
    prefix="/api/schemes",
    tags=["Government Schemes"]
)


SCHEMES = [
    {
        "id": 1,
        "name": "PM-KISAN",
        "full_name": "Pradhan Mantri Kisan Samman Nidhi",
        "category": "Income Support",
        "description": (
            "Central Government income-support scheme for eligible "
            "landholding farmer families."
        ),
        "benefit": (
            "Eligible beneficiaries can receive financial support "
            "as per the current government scheme rules."
        ),
        "eligibility": (
            "Landholding farmer families who satisfy the current "
            "government eligibility and exclusion criteria."
        ),
        "documents": [
            "Aadhaar",
            "Mobile number",
            "Bank account details",
            "Land-related details"
        ],
        "application_mode": "Online / Common Service Centre",
        "official_source": "PM-KISAN Official Portal",
        "official_url": "https://pmkisan.gov.in/"
    },

    {
        "id": 2,
        "name": "PMFBY",
        "full_name": "Pradhan Mantri Fasal Bima Yojana",
        "category": "Crop Insurance",
        "description": (
            "Crop insurance scheme designed to provide financial support "
            "against eligible crop losses."
        ),
        "benefit": (
            "Insurance protection against specified crop losses "
            "subject to scheme rules and notified crops."
        ),
        "eligibility": (
            "Farmers cultivating crops covered under the scheme "
            "in notified areas and seasons."
        ),
        "documents": [
            "Aadhaar",
            "Mobile number",
            "Bank account details",
            "Land or tenancy details",
            "Crop details"
        ],
        "application_mode": "Online / Bank / Common Service Centre",
        "official_source": "PMFBY Official Portal",
        "official_url": "https://pmfby.gov.in/"
    },

    {
        "id": 3,
        "name": "Soil Health Card",
        "full_name": "Soil Health Card Scheme",
        "category": "Soil Health",
        "description": (
            "Provides farmers with information about soil nutrient status "
            "and recommendations for balanced nutrient management."
        ),
        "benefit": (
            "Provides soil-test information and nutrient recommendations "
            "to support better soil and crop management."
        ),
        "eligibility": (
            "Farmers seeking soil testing and soil-health guidance."
        ),
        "documents": [
            "Farmer details",
            "Mobile number",
            "Land or field details"
        ],
        "application_mode": (
            "Agriculture Department / Soil Testing Laboratory / "
            "Local agricultural service centre"
        ),
        "official_source": "Soil Health Card Portal",
        "official_url": "https://soilhealth.dac.gov.in/"
    }
]


@router.get("/")
def get_all_schemes():

    return {
        "status": "success",
        "total_schemes": len(SCHEMES),
        "schemes": SCHEMES,
        "note": (
            "Scheme benefits, eligibility rules, documents and application "
            "periods may change. Always verify the latest information on the "
            "official government portal before applying."
        )
    }


@router.get("/{scheme_id}")
def get_scheme(scheme_id: int):

    for scheme in SCHEMES:
        if scheme["id"] == scheme_id:
            return {
                "status": "success",
                "scheme": scheme,
                "note": (
                    "Please verify the latest scheme details on the official "
                    "government portal before applying."
                )
            }

    raise HTTPException(
        status_code=404,
        detail="Scheme not found."
    )