from backend.services.care_scheduler import get_care_schedule
from backend.services.alert_service import generate_alert
from backend.services.weather_api import get_current_weather
from backend.services.weather_risk import calculate_weather_risk
from database.database import save_disease_history, get_disease_history
from fastapi import APIRouter, UploadFile, File, HTTPException
from ultralytics import YOLO
from pathlib import Path
from backend.services.recommendation import get_recommendation
from backend.services.health_score import calculate_health_score
import tempfile
import os


router = APIRouter(
    prefix="/api/disease",
    tags=["Disease Detection"]
)


# Path to trained CareBloom model
MODEL_PATH = Path(__file__).resolve().parent.parent / "models" / "best.pt"

# Load model once when backend starts
model = YOLO(str(MODEL_PATH))

@router.post("/predict")
async def predict_disease(
    user_id: int,
    file: UploadFile = File(...)
):

    # Allow only JPG and PNG images
    if file.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(
            status_code=400,
            detail="Please upload a JPG or PNG image."
        )

    temp_path = None

    try:
        # Save uploaded image temporarily
        suffix = Path(file.filename or "image.jpg").suffix or ".jpg"

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix
        ) as temp_file:

            image_data = await file.read()
            temp_file.write(image_data)
            temp_path = temp_file.name

        # Run CareBloom AI prediction
        results = model.predict(
            source=temp_path,
            verbose=False
        )

        result = results[0]

        # Get predicted class and confidence
        class_id = result.probs.top1
        confidence = result.probs.top1conf.item()
        class_name = result.names[class_id]

        # Convert confidence to percentage
        confidence_percent = round(confidence * 100, 2)

        # Clean model class name
        clean_name = class_name.replace("___", "__").replace("_", " ")

        parts = clean_name.split("  ", 1)

        if len(parts) == 2:
            plant = parts[0].strip()
            disease = parts[1].strip()
        else:
            plant = "Unknown"
            disease = clean_name.strip()

        # Get treatment recommendation
        recommendation = get_recommendation(
            plant,
            disease
        )

        # Calculate plant health score
        health = calculate_health_score(
            disease,
            confidence_percent
        )
        live_weather = get_current_weather(
            latitude=13.0827,
            longitude=80.2707
        )

        weather = calculate_weather_risk(
            temperature=live_weather["temperature"],
            humidity=live_weather["humidity"],
            rainfall=live_weather["rainfall"]
        )
        alert = generate_alert(
            weather_risk=weather["weather_risk"],
            health_status=health["health_status"]
        )
        care_schedule = get_care_schedule(plant)

        # Save prediction to database
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

        # Send final response
        return {
            "filename": file.filename,
            "plant": plant,
            "disease": disease,
            "confidence": confidence_percent,
            "health_score": health["health_score"],
            "health_status": health["health_status"],
            "temperature": live_weather["temperature"],
            "humidity": live_weather["humidity"],
            "rainfall": live_weather["rainfall"],
            "weather_risk": weather["weather_risk"],
            "weather_risk_score": weather["risk_score"],
            "alert_level": alert["alert_level"],
            "alert_message": alert["alert_message"],
            "watering_interval_days": care_schedule["watering_interval_days"],
            "next_watering_date": care_schedule["next_watering_date"],
            "fertilizer_interval_days": care_schedule["fertilizer_interval_days"],
            "next_fertilizer_date": care_schedule["next_fertilizer_date"],
            "organic_remedy": recommendation["organic_remedy"],
            "chemical_treatment": recommendation["chemical_treatment"],
            "prevention": recommendation["prevention"]
        }

    finally:
        # Delete temporary uploaded image
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


@router.get("/history")
def disease_history(user_id: int):
    return get_disease_history(user_id)