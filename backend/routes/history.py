from fastapi import APIRouter, HTTPException
from collections import Counter, defaultdict
from datetime import datetime

from database.database import get_disease_history


router = APIRouter(
    prefix="/api/history",
    tags=["Disease History"]
)


# ============================================================
# GET FULL USER HISTORY
# ============================================================

@router.get("/user/{user_id}")
def get_user_history(user_id: int):

    try:
        history = get_disease_history(user_id)

        return {
            "status": "success",
            "user_id": user_id,
            "total_scans": len(history),
            "history": history
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to load disease history: {str(error)}"
        )


# ============================================================
# CALENDAR VIEW
# ============================================================

@router.get("/calendar/{user_id}")
def get_history_calendar(user_id: int):

    try:
        history = get_disease_history(user_id)

        calendar = defaultdict(list)

        for item in history:

            created_at = item.get("created_at")

            if not created_at:
                continue

            try:
                date = datetime.fromisoformat(
                    str(created_at)
                ).strftime("%Y-%m-%d")

            except Exception:
                date = str(created_at).split(" ")[0]

            calendar[date].append({
                "scan_id": item["id"],
                "plant": item["plant"],
                "disease": item["disease"],
                "confidence": item["confidence"],
                "health_score": item["health_score"],
                "health_status": item["health_status"]
            })

        return {
            "status": "success",
            "user_id": user_id,
            "calendar": dict(calendar)
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to build history calendar: {str(error)}"
        )


# ============================================================
# USER HISTORY STATISTICS
# ============================================================

@router.get("/stats/{user_id}")
def get_history_stats(user_id: int):

    try:
        history = get_disease_history(user_id)

        total_scans = len(history)

        healthy_count = 0
        diseased_count = 0

        disease_names = []

        health_scores = []

        for item in history:

            disease = str(
                item.get("disease", "")
            ).strip()

            if "healthy" in disease.lower():
                healthy_count += 1
            else:
                diseased_count += 1

                if disease:
                    disease_names.append(disease)

            score = item.get("health_score")

            if score is not None:
                health_scores.append(score)

        common_diseases = Counter(
            disease_names
        ).most_common(5)

        average_health_score = None

        if health_scores:
            average_health_score = round(
                sum(health_scores) / len(health_scores),
                2
            )

        return {
            "status": "success",
            "user_id": user_id,
            "total_scans": total_scans,
            "healthy_scans": healthy_count,
            "diseased_scans": diseased_count,
            "average_health_score": average_health_score,
            "most_common_diseases": [
                {
                    "disease": disease,
                    "count": count
                }
                for disease, count in common_diseases
            ]
        }

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Unable to calculate history statistics: {str(error)}"
        )


# ============================================================
# SERVICE STATUS
# ============================================================

@router.get("/")
def history_service_status():

    return {
        "status": "running",
        "service": "CareBloom Disease History Service"
    }