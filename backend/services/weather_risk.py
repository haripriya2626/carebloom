def calculate_weather_risk(temperature: float, humidity: float, rainfall: float):
    score = 0

    if humidity >= 80:
        score += 2
    elif humidity >= 65:
        score += 1

    if 20 <= temperature <= 30:
        score += 1

    if rainfall >= 10:
        score += 2
    elif rainfall > 0:
        score += 1

    if score >= 4:
        risk = "High"
    elif score >= 2:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "weather_risk": risk,
        "risk_score": score
    }