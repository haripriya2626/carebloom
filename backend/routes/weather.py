from fastapi import APIRouter, HTTPException

from backend.services.weather_api import get_current_weather
from backend.services.weather_risk import calculate_weather_risk
from backend.services.alert_service import generate_alert


router = APIRouter(
    prefix="/api/weather",
    tags=["Weather & Disease Risk"]
)


@router.get("/risk")
def get_weather_risk(
    latitude: float,
    longitude: float
):
    """
    Get current weather,
    calculate plant disease risk,
    and generate an alert.
    """

    try:

        # Get live weather
        weather_data = get_current_weather(
            latitude=latitude,
            longitude=longitude
        )

        # Calculate disease risk
        risk = calculate_weather_risk(
            temperature=weather_data["temperature"],
            humidity=weather_data["humidity"],
            rainfall=weather_data["rainfall"]
        )

        # Generate alert
        alert = generate_alert(
            weather_risk=risk["weather_risk"],
            health_status="Moderate"
        )

        return {
            "status": "success",

            "location": {
                "latitude": latitude,
                "longitude": longitude
            },

            "weather": {
                "temperature": weather_data["temperature"],
                "humidity": weather_data["humidity"],
                "rainfall": weather_data["rainfall"]
            },

            "disease_risk": {
                "risk_level": risk["weather_risk"],
                "risk_score": risk["risk_score"]
            },

            "alert": {
                "alert_level": alert["alert_level"],
                "alert_message": alert["alert_message"]
            }
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Weather risk analysis failed: {str(error)}"
        )


@router.get("/")
def weather_service_status():

    return {
        "status": "running",
        "service": "CareBloom Weather Risk Engine"
    }