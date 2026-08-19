
def calculate_health_score(disease: str, confidence: float):

    # Healthy plant
    if "healthy" in disease.lower():
        return {
            "health_score": 95,
            "health_status": "Excellent"
        }

    # Disease detected with high confidence
    if confidence >= 90:
        return {
            "health_score": 50,
            "health_status": "Poor"
        }

    # Disease detected with medium confidence
    elif confidence >= 70:
        return {
            "health_score": 65,
            "health_status": "Moderate"
        }

    # Disease detected with lower confidence
    else:
        return {
            "health_score": 75,
            "health_status": "Fair"
        }