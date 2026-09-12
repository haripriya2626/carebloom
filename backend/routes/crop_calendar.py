from fastapi import APIRouter, HTTPException
from datetime import datetime


router = APIRouter(
    prefix="/api/crop-calendar",
    tags=["Crop Calendar"]
)


# ============================================================
# CROP CALENDAR DATA
# General seasonal guidance for the first version.
# ============================================================

CROP_CALENDAR = {

    "Rice": {
        "seasons": ["Kharif", "Rabi"],
        "sowing_months": ["June", "July", "November", "December"],
        "harvest_months": ["October", "November", "March", "April"],
        "duration_days": "100-150",
        "care_tips": [
            "Maintain suitable field moisture",
            "Monitor for blast and bacterial leaf diseases",
            "Apply nutrients according to crop stage",
            "Control weeds during early growth"
        ]
    },

    "Wheat": {
        "seasons": ["Rabi"],
        "sowing_months": ["October", "November", "December"],
        "harvest_months": ["March", "April"],
        "duration_days": "110-150",
        "care_tips": [
            "Use healthy seed",
            "Monitor for rust diseases",
            "Avoid unnecessary irrigation",
            "Apply fertilizer based on soil and crop needs"
        ]
    },

    "Maize": {
        "seasons": ["Kharif", "Rabi"],
        "sowing_months": ["June", "July", "October", "November"],
        "harvest_months": ["September", "October", "February", "March"],
        "duration_days": "90-120",
        "care_tips": [
            "Maintain good field drainage",
            "Monitor for leaf blight and rust",
            "Control weeds during early growth",
            "Monitor soil moisture"
        ]
    },

    "Tomato": {
        "seasons": ["Multiple seasons"],
        "sowing_months": [
            "January",
            "June",
            "July",
            "October",
            "November"
        ],
        "harvest_months": [
            "March",
            "April",
            "September",
            "December"
        ],
        "duration_days": "90-140",
        "care_tips": [
            "Maintain consistent soil moisture",
            "Avoid prolonged leaf wetness",
            "Monitor regularly for blight and leaf spot",
            "Provide suitable plant support"
        ]
    },

    "Potato": {
        "seasons": ["Rabi"],
        "sowing_months": ["October", "November"],
        "harvest_months": ["January", "February", "March"],
        "duration_days": "90-120",
        "care_tips": [
            "Use healthy planting material",
            "Avoid waterlogging",
            "Monitor for early and late blight",
            "Maintain suitable soil moisture"
        ]
    },

    "Groundnut": {
        "seasons": ["Kharif", "Rabi"],
        "sowing_months": ["June", "July", "November", "December"],
        "harvest_months": ["September", "October", "February", "March"],
        "duration_days": "100-130",
        "care_tips": [
            "Maintain good soil drainage",
            "Monitor for leaf spot and rust",
            "Control weeds during early growth",
            "Avoid excessive irrigation"
        ]
    },

    "Sugarcane": {
        "seasons": ["Annual"],
        "sowing_months": ["January", "February", "March", "October"],
        "harvest_months": ["December", "January", "February", "March"],
        "duration_days": "300-365",
        "care_tips": [
            "Maintain suitable irrigation",
            "Monitor for red rot",
            "Remove heavily affected plants",
            "Apply nutrients based on field requirements"
        ]
    },

    "Banana": {
        "seasons": ["Year-round where suitable"],
        "sowing_months": [
            "January",
            "February",
            "June",
            "July",
            "August",
            "September"
        ],
        "harvest_months": ["Depends on planting date"],
        "duration_days": "300-450",
        "care_tips": [
            "Maintain adequate soil moisture",
            "Avoid waterlogging",
            "Monitor leaves for Sigatoka symptoms",
            "Remove severely infected leaves when appropriate"
        ]
    }
}


# ============================================================
# GET ALL CROPS
# ============================================================

@router.get("/")
def get_crop_calendar():

    return {
        "status": "success",
        "total_crops": len(CROP_CALENDAR),
        "crops": CROP_CALENDAR,
        "note": (
            "Crop seasons and timings vary by location, variety, "
            "weather and farming practices. These values are "
            "general guidance."
        )
    }


# ============================================================
# GET ONE CROP
# ============================================================

@router.get("/crop/{crop_name}")
def get_crop_details(crop_name: str):

    normalized_name = crop_name.strip().title()

    crop = CROP_CALENDAR.get(normalized_name)

    if crop is None:

        raise HTTPException(
            status_code=404,
            detail="Crop calendar information not found."
        )

    return {
        "status": "success",
        "crop": normalized_name,
        "calendar": crop
    }


# ============================================================
# CURRENT MONTH RECOMMENDATIONS
# ============================================================

@router.get("/current/recommendations")
def current_crop_recommendations():

    current_month = datetime.now().strftime("%B")

    sowing_crops = []
    harvest_crops = []

    for crop_name, data in CROP_CALENDAR.items():

        if current_month in data["sowing_months"]:
            sowing_crops.append(crop_name)

        if current_month in data["harvest_months"]:
            harvest_crops.append(crop_name)

    return {
        "status": "success",
        "current_month": current_month,
        "recommended_for_sowing": sowing_crops,
        "possible_harvest": harvest_crops,
        "note": (
            "Recommendations are general. Actual crop calendars "
            "should consider the user's region, weather, crop "
            "variety and local agricultural guidance."
        )
    }
