def generate_alert(weather_risk: str, health_status: str):

    if weather_risk == "High" or health_status == "Poor":
        return {
            "alert_level": "High",
            "alert_message": "Immediate attention is recommended. Monitor the plant and apply suitable treatment."
        }

    elif weather_risk == "Medium":
        return {
            "alert_level": "Medium",
            "alert_message": "Moderate disease risk detected. Monitor the plant closely."
        }

    else:
        return {
            "alert_level": "Low",
            "alert_message": "Plant conditions are currently stable. Continue regular care."
        }