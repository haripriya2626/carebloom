from fastapi import APIRouter, HTTPException
from math import radians, sin, cos, sqrt, atan2
import requests


router = APIRouter(
    prefix="/api/nearby",
    tags=["Nearby Agricultural Services"]
)


# ============================================================
# CONFIG
# ============================================================

OVERPASS_URL = "https://overpass-api.de/api/interpreter"

HEADERS = {
    "User-Agent": "CareBloom-Final-Year-Project/1.0"
}


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
# BUILD OVERPASS QUERY
# ============================================================

def build_overpass_query(
    latitude: float,
    longitude: float,
    radius_m: int,
    category: str
):

    category_filters = {

        "agriculture_office": [
            'office="government"',
            'government="agriculture"'
        ],

        "soil_testing": [
            'name~"soil|Soil|agriculture|Agriculture"'
        ],

        "nursery": [
            'shop="garden_centre"',
            'shop="agrarian"'
        ],

        "seed_store": [
            'shop="agrarian"',
            'name~"seed|Seed|seeds|Seeds"'
        ],

        "fertilizer_store": [
            'shop="agrarian"',
            'name~"fertilizer|Fertilizer|fertiliser|Fertiliser"'
        ],

        "plant_clinic": [
            'name~"plant clinic|Plant Clinic|agriculture clinic|Agriculture Clinic"'
        ]
    }

    filters = []

    if category == "all":

        for values in category_filters.values():
            filters.extend(values)

    else:
        filters = category_filters.get(category, [])

    query_parts = []

    for item in filters:

        if "=" in item and "~" not in item:

            key, value = item.split("=", 1)

            query_parts.append(
                f'node(around:{radius_m},{latitude},{longitude})'
                f'[{key}={value}];'
            )

            query_parts.append(
                f'way(around:{radius_m},{latitude},{longitude})'
                f'[{key}={value}];'
            )

        else:

            key, value = item.split("~", 1)

            query_parts.append(
                f'node(around:{radius_m},{latitude},{longitude})'
                f'[{key}~{value},i];'
            )

            query_parts.append(
                f'way(around:{radius_m},{latitude},{longitude})'
                f'[{key}~{value},i];'
            )

    return f"""
    [out:json][timeout:20];
    (
        {''.join(query_parts)}
    );
    out center tags;
    """


# ============================================================
# FORMAT OSM RESULT
# ============================================================

def format_service(
    element: dict,
    user_latitude: float,
    user_longitude: float
):

    tags = element.get("tags", {})

    latitude = element.get("lat")
    longitude = element.get("lon")

    if latitude is None or longitude is None:

        center = element.get("center", {})

        latitude = center.get("lat")
        longitude = center.get("lon")

    if latitude is None or longitude is None:
        return None

    name = tags.get("name")

    if not name:
        return None

    distance = calculate_distance(
        user_latitude,
        user_longitude,
        latitude,
        longitude
    )

    address_parts = [
        tags.get("addr:housenumber"),
        tags.get("addr:street"),
        tags.get("addr:suburb"),
        tags.get("addr:city"),
        tags.get("addr:district")
    ]

    address = ", ".join(
        part
        for part in address_parts
        if part
    )

    return {
        "name": name,
        "latitude": latitude,
        "longitude": longitude,
        "distance_km": distance,
        "address": address or None,
        "phone": tags.get("phone") or tags.get("contact:phone"),
        "website": tags.get("website") or tags.get("contact:website"),
        "osm_type": element.get("type"),
        "osm_id": element.get("id")
    }


# ============================================================
# FETCH LIVE SERVICES
# ============================================================

def fetch_nearby_services(
    latitude: float,
    longitude: float,
    radius_km: float,
    category: str
):

    radius_m = int(radius_km * 1000)

    query = build_overpass_query(
        latitude,
        longitude,
        radius_m,
        category
    )

    try:

        response = requests.post(
            OVERPASS_URL,
            data={"data": query},
            headers=HEADERS,
            timeout=25
        )

        response.raise_for_status()

        data = response.json()

        services = []

        seen = set()

        for element in data.get("elements", []):

            service = format_service(
                element,
                latitude,
                longitude
            )

            if not service:
                continue

            unique_key = (
                service["name"].lower(),
                round(service["latitude"], 5),
                round(service["longitude"], 5)
            )

            if unique_key in seen:
                continue

            seen.add(unique_key)

            services.append(service)

        services.sort(
            key=lambda item: item["distance_km"]
        )

        return services

    except (
        requests.RequestException,
        ValueError
    ):
        return None


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

    # ----------------------------
    # Validate latitude
    # ----------------------------

    if latitude < -90 or latitude > 90:

        raise HTTPException(
            status_code=400,
            detail="Latitude must be between -90 and 90."
        )


    # ----------------------------
    # Validate longitude
    # ----------------------------

    if longitude < -180 or longitude > 180:

        raise HTTPException(
            status_code=400,
            detail="Longitude must be between -180 and 180."
        )


    # ----------------------------
    # Validate radius
    # ----------------------------

    if radius_km <= 0 or radius_km > 50:

        raise HTTPException(
            status_code=400,
            detail="Radius must be between 0 and 50 km."
        )


    # ----------------------------
    # Validate category
    # ----------------------------

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


    # ----------------------------
    # Fetch live services
    # ----------------------------

    services = fetch_nearby_services(
        latitude,
        longitude,
        radius_km,
        category
    )


    # Provider temporarily unavailable

    if services is None:

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
            "data_status": "provider_temporarily_unavailable",
            "message": (
                "The live OpenStreetMap nearby service "
                "provider is temporarily unavailable."
            )
        }


    # No places found

    if not services:

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
            "data_status": "live",
            "source": "OpenStreetMap",
            "message": (
                "No matching agricultural services were found "
                "within the selected radius."
            )
        }


    # Successful result

    return {
        "status": "success",
        "location": {
            "latitude": latitude,
            "longitude": longitude
        },
        "category": category,
        "radius_km": radius_km,
        "total_results": len(services),
        "services": services,
        "data_status": "live",
        "source": "OpenStreetMap"
    }


# ============================================================
# SERVICE STATUS
# ============================================================

@router.get("/")
def nearby_service_status():

    return {
        "status": "running",
        "service": "CareBloom Nearby Agricultural Services",
        "live_provider": "OpenStreetMap / Overpass API",
        "live_provider_connected": True
    }