from datetime import datetime, timedelta


def get_care_schedule(plant: str):
    today = datetime.now()

    schedules = {
        "Tomato": {
            "water_interval_days": 2,
            "fertilizer_interval_days": 14
        },
        "Potato": {
            "water_interval_days": 3,
            "fertilizer_interval_days": 21
        },
        "Pepper": {
            "water_interval_days": 2,
            "fertilizer_interval_days": 14
        }
    }

    default_schedule = {
        "water_interval_days": 3,
        "fertilizer_interval_days": 21
    }

    schedule = schedules.get(plant, default_schedule)

    next_watering = today + timedelta(
        days=schedule["water_interval_days"]
    )

    next_fertilizer = today + timedelta(
        days=schedule["fertilizer_interval_days"]
    )

    return {
        "watering_interval_days": schedule["water_interval_days"],
        "next_watering_date": next_watering.strftime("%Y-%m-%d"),
        "fertilizer_interval_days": schedule["fertilizer_interval_days"],
        "next_fertilizer_date": next_fertilizer.strftime("%Y-%m-%d")
    }