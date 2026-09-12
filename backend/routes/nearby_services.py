from fastapi import APIRouter, HTTPException
from math import radians, sin, cos, sqrt, atan2


router = APIRouter(
    prefix="/api/nearby",
    tags=["Nearby Agricultural Services"]
)


# ============================================================
# SERVICE CATEGORIES
# ============================================================

SERVICE_CATEGORIES = [
    {
        "id": "agriculture_office",
        "name": "Agriculture Office"
    },
    {
        "id": "soil_testing",
        "name": "Soil Testing Centre"
    },
    {
        "id": "nursery",
        "name": "Plant Nursery"
    },
    {
        "id": "seed_store",
        "name": "Seed Store"
    },
    {
        "id": "fertilizer_store",
        "name": "Fertilizer Store"
    },
    {
        "id": "plant_clinic",
        "name": "Plant Clinic"
    }
]


# ============================================================
# DISTANCE CALCULATOR
# ============================================================

def calculate_distance(
    latitude1: float,
    longitude1: float,
    latitude2: float,
    longitude2: float
):

    earth_radius = 6371

    lat1 = radians(latitude1)
    lon1 = radians(longitude1)

    lat2 = radians(latitude2)
    lon2 = radians(longitude2)

    latitude_difference = lat2 - lat1
    longitude_difference = lon2 - lon1

    a = (
        sin(latitude_difference / 2) ** 2
        +
        cos(lat1)
        * cos(lat2)
        * sin(longitude_difference / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return round(
        earth_radius * c,
        2
    )


# ============================================================
# GET AVAILABLE SERVICE TYPES
# ============================================================

@router.get("/categories")
def get_service_categories():

    return {
        "status": "success",
        "total_categories": len(SERVICE_CATEGORIES),
        "categories": SERVICE_CATEGORIES
    }


# ============================================================
# NEARBY SEARCH
# ============================================================

@router.get("/search")
def search_nearby_services(
    latitude: float,
    longitude: float,
    category: str = "all",
    radius_km: float = 10
):

    # Validate latitude

    if latitude < -90 or latitude > 90:

        raise HTTPException(
            status_code=400,
            detail="Latitude must be between -90 and 90."
        )


    # Validate longitude

    if longitude < -180 or longitude > 180:

        raise HTTPException(
            status_code=400,
            detail="Longitude must be between -180 and 180."
        )


    # Validate radius

    if radius_km <= 0 or radius_km > 100:

        raise HTTPException(
            status_code=400,
            detail="Radius must be between 0 and 100 km."
        )


    valid_categories = [
        item["id"]
        for item in SERVICE_CATEGORIES
    ]

    if (
        category != "all"
        and category not in valid_categories
    ):

        raise HTTPException(
            status_code=400,
            detail="Invalid service category."
        )


    # Real provider integration will be added later.
    # We intentionally return no fabricated businesses.

    return {
        "status": "success",
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "category": category,
        "radius_km": radius_km,
        "total_results": 0,
        "services": [],
        "data_status": "provider_not_connected",
        "message": (
            "Location search is ready, but a live places "
            "provider has not yet been connected."
        )
    }


# ============================================================
# SERVICE STATUS
# ============================================================

@router.get("/")
def nearby_service_status():

    return {
        "status": "running",
        "service": "CareBloom Nearby Agricultural Services",
        "live_provider_connected": False
    }