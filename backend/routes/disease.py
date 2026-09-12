from fastapi import APIRouter, UploadFile, File, HTTPException
from ultralytics import YOLO
from pathlib import Path

from backend.services.care_scheduler import get_care_schedule
from backend.services.alert_service import generate_alert
from backend.services.weather_api import get_current_weather
from backend.services.weather_risk import calculate_weather_risk
from backend.services.recommendation import get_recommendation
from backend.services.health_score import calculate_health_score

from database.database import (
    save_disease_history,
    get_disease_history
)

import tempfile
import os


# ============================================================
# ROUTER
# ============================================================

router = APIRouter(
    prefix="/api/disease",
    tags=["Disease Detection"]
)


# ============================================================
# MODEL
# ============================================================

MODEL_PATH = (
    Path(__file__).resolve().parent.parent
    / "models"
    / "best.pt"
)

if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"CareBloom model not found: {MODEL_PATH}"
    )

# Load model once when backend starts
model = YOLO(str(MODEL_PATH))


# ============================================================
# HELPERS
# ============================================================

def clean_prediction_name(class_name: str):
    """
    Convert YOLO class names such as:

    Tomato___Late_Blight

    into:

    plant = Tomato
    disease = Late Blight
    """

    class_name = class_name.strip()

    if "___" in class_name:
        plant, disease = class_name.split("___", 1)

        plant = plant.replace("_", " ").strip()
        disease = disease.replace("_", " ").strip()

        return plant, disease

    # Fallback if class naming is different
    clean_name = class_name.replace("_", " ").strip()

    return "Unknown", clean_name


# ============================================================
# DISEASE PREDICTION
# ============================================================

@router.post("/predict")
async def predict_disease(
    user_id: int,
    file: UploadFile = File(...)
):

    # --------------------------------------------------------
    # FILE VALIDATION
    # --------------------------------------------------------

    allowed_types = [
        "image/jpeg",
        "image/png"
    ]

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG or PNG image."
        )

    temp_path = None

    try:

        # ----------------------------------------------------
        # SAVE IMAGE TEMPORARILY
        # ----------------------------------------------------

        suffix = (
            Path(file.filename or "image.jpg").suffix
            or ".jpg"
        )

        image_data = await file.read()

        if not image_data:
            raise HTTPException(
                status_code=400,
                detail="Uploaded image is empty."
            )

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            temp_file.write(image_data)

            temp_path = temp_file.name


        # ----------------------------------------------------
        # YOLO PREDICTION
        # ----------------------------------------------------

        results = model.predict(
            source=temp_path,
            verbose=False
        )

        if not results:
            raise HTTPException(
                status_code=500,
                detail="Disease prediction failed."
            )

        result = results[0]

        if result.probs is None:
            raise HTTPException(
                status_code=500,
                detail="Model did not return classification probabilities."
            )


        # ----------------------------------------------------
        # GET TOP PREDICTION
        # ----------------------------------------------------

        class_id = int(result.probs.top1)

        confidence = float(
            result.probs.top1conf.item()
        )

        confidence_percent = round(
            confidence * 100,
            2
        )

        class_name = result.names[class_id]
        print("RAW MODEL CLASS:", repr(class_name))


        # ----------------------------------------------------
        # CLEAN CLASS NAME
        # ----------------------------------------------------

        plant, disease = clean_prediction_name(
            class_name
        )


        # ----------------------------------------------------
        # LOW CONFIDENCE HANDLING
        # ----------------------------------------------------

        LOW_CONFIDENCE_THRESHOLD = 50.0

        if confidence_percent < LOW_CONFIDENCE_THRESHOLD:

            return {
                "filename": file.filename,
                "plant": plant,
                "disease": disease,
                "confidence": confidence_percent,
                "status": "low_confidence",
                "message": (
                    "CareBloom could not identify this leaf "
                    "with enough confidence. Please upload a "
                    "clearer leaf image."
                )
            }


        # ----------------------------------------------------
        # TREATMENT RECOMMENDATION
        # ----------------------------------------------------

        recommendation = get_recommendation(
            plant,
            disease
        )


        # ----------------------------------------------------
        # HEALTH SCORE
        # ----------------------------------------------------

        health = calculate_health_score(
            disease,
            confidence_percent
        )


        # ----------------------------------------------------
        # WEATHER DATA
        # ----------------------------------------------------

        # Temporary default coordinates
        # Later frontend can send user's actual latitude/longitude

        live_weather = get_current_weather(
            latitude=13.0827,
            longitude=80.2707
        )


        # ----------------------------------------------------
        # WEATHER DISEASE RISK
        # ----------------------------------------------------

        weather = calculate_weather_risk(
            temperature=live_weather["temperature"],
            humidity=live_weather["humidity"],
            rainfall=live_weather["rainfall"]
        )


        # ----------------------------------------------------
        # ALERT
        # ----------------------------------------------------

        alert = generate_alert(
    weather_risk=weather["weather_risk"],
    health_status=health["health_status"],
    disease=disease
)
        # ----------------------------------------------------
        # CARE SCHEDULE
        # ----------------------------------------------------

        care_schedule = get_care_schedule(
            plant
        )


        # ----------------------------------------------------
        # SAVE HISTORY
        # ----------------------------------------------------

        save_disease_history(
            user_id=user_id,
            filename=file.filename,
            plant=plant,
            disease=disease,
            confidence=confidence_percent,
            health_score=health["health_score"],
            health_status=health["health_status"],
            organic_remedy=recommendation["organic_remedy"],
            chemical_treatment=recommendation["chemical_treatment"],
            prevention=recommendation["prevention"]
        )


        # ----------------------------------------------------
        # FINAL API RESPONSE
        # ----------------------------------------------------

        return {

            "status": "success",

            "filename": file.filename,

            "prediction": {
                "plant": plant,
                "disease": disease,
                "confidence": confidence_percent
            },

            "plant_health": {
                "health_score": health["health_score"],
                "health_status": health["health_status"]
            },

            "weather": {
                "temperature": live_weather["temperature"],
                "humidity": live_weather["humidity"],
                "rainfall": live_weather["rainfall"]
            },

            "disease_risk": {
                "weather_risk": weather["weather_risk"],
                "weather_risk_score": weather["risk_score"]
            },

            "alert": {
                "alert_level": alert["alert_level"],
                "alert_message": alert["alert_message"]
            },

            "care_schedule": {
                "watering_interval_days":
                    care_schedule["watering_interval_days"],

                "next_watering_date":
                    care_schedule["next_watering_date"],

                "fertilizer_interval_days":
                    care_schedule["fertilizer_interval_days"],

                "next_fertilizer_date":
                    care_schedule["next_fertilizer_date"]
            },

            "recommendation": {
                "organic_remedy":
                    recommendation["organic_remedy"],

                "chemical_treatment":
                    recommendation["chemical_treatment"],

                "prevention":
                    recommendation["prevention"]
            }
        }


    except HTTPException:
        raise


    except Exception as error:

        print(
            "Disease prediction error:",
            str(error)
        )

        raise HTTPException(
            status_code=500,
            detail=f"Disease prediction failed: {str(error)}"
        )


    finally:

        # ----------------------------------------------------
        # DELETE TEMP IMAGE
        # ----------------------------------------------------

        if (
            temp_path
            and os.path.exists(temp_path)
        ):

            try:
                os.remove(temp_path)

            except Exception:
                pass


# ============================================================
# DISEASE HISTORY
# ============================================================

@router.get("/history")
def disease_history(
    user_id: int
):

    try:

        return {
            "user_id": user_id,
            "history": get_disease_history(
                user_id
            )
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=f"Unable to load disease history: {str(error)}"
        )