def calculate_health_score(disease: str, confidence: float):

    disease_lower = disease.lower()

    # Healthy plant
    if "healthy" in disease_lower:
        return {
            "health_score": 95,
            "health_status": "Excellent"
        }

    # Severe/high-impact disease categories
    severe_keywords = [
        "blight",
        "wilt",
        "rot",
        "smut",
        "blast",
        "greening",
        "bunchy top",
        "tungro"
    ]

    # Moderate disease categories
    moderate_keywords = [
        "rust",
        "mildew",
        "spot",
        "scab",
        "canker",
        "anthracnose",
        "mosaic",
        "curl",
        "crinkle"
    ]

    if any(word in disease_lower for word in severe_keywords):
        return {
            "health_score": 55,
            "health_status": "Needs Attention"
        }

    elif any(word in disease_lower for word in moderate_keywords):
        return {
            "health_score": 70,
            "health_status": "Monitor"
        }

    else:
        return {
            "health_score": 75,
            "health_status": "Monitor"
        }