def generate_alert(weather_risk: str, health_status: str, disease: str = ""):

    # Healthy plant should not show a disease warning
    if "healthy" in disease.lower():
        return {
            "alert_level": "Low",
            "alert_message": (
                "Plant appears healthy. "
                "Continue regular monitoring and care."
            )
        }

    # High-risk condition
    if weather_risk == "High" or health_status == "Needs Attention":
        return {
            "alert_level": "High",
            "alert_message": (
                "Immediate attention is recommended. "
                "Monitor the plant and apply suitable treatment."
            )
        }

    # Medium-risk condition
    elif weather_risk == "Medium" or health_status == "Monitor":
        return {
            "alert_level": "Medium",
            "alert_message": (
                "Moderate disease risk detected. "
                "Monitor the plant closely and follow preventive care."
            )
        }

    # Low-risk / stable condition
    else:
        return {
            "alert_level": "Low",
            "alert_message": (
                "Plant conditions are currently stable. "
                "Continue regular care and monitoring."
            )
        }