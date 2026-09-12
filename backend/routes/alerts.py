from fastapi import APIRouter, HTTPException

from backend.services.alert_service import generate_alert


router = APIRouter(
    prefix="/api/alerts",
    tags=["Emergency Alerts"]
)


@router.get("/disease")
def get_disease_alert(
    weather_risk: str,
    health_status: str
):
    """
    Generate an emergency disease alert
    based on weather risk and plant health.
    """

    try:

        weather_risk = weather_risk.strip().title()
        health_status = health_status.strip().title()


        valid_risks = ["Low", "Medium", "High"]
        valid_health = [
            "Excellent",
            "Good",
            "Moderate",
            "Poor",
            "Critical"
        ]

        if weather_risk not in valid_risks:
            raise HTTPException(
                status_code=400,
                detail="weather_risk must be Low, Medium, or High."
            )

        if health_status not in valid_health:
            raise HTTPException(
                status_code=400,
                detail=(
                    "health_status must be Excellent, Good, "
                    "Moderate, Poor, or Critical."
                )
            )

        alert = generate_alert(
            weather_risk=weather_risk,
            health_status=health_status
        )

        return {
            "status": "success",
            "weather_risk": weather_risk,
            "health_status": health_status,
            "alert": {
                "alert_level": alert["alert_level"],
                "alert_message": alert["alert_message"]
            }
        }

    except HTTPException:
        raise

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to generate disease alert: {str(error)}"
        )


@router.get("/")
def alert_service_status():

    return {
        "status": "running",
        "service": "CareBloom Emergency Alert Engine"
    }