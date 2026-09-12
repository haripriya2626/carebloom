from datetime import datetime, timedelta


# ============================================================
# BASE CARE SCHEDULES
# These are general starting intervals.
# Weather and plant conditions can modify them later.
# ============================================================

CARE_SCHEDULES = {

    "Tomato": {
        "water_interval_days": 2,
        "fertilizer_interval_days": 14
    },

    "Potato": {
        "water_interval_days": 3,
        "fertilizer_interval_days": 21
    },

    "Bell Pepper": {
        "water_interval_days": 2,
        "fertilizer_interval_days": 14
    },

    "Chilli": {
        "water_interval_days": 2,
        "fertilizer_interval_days": 14
    },

    "Rice": {
        "water_interval_days": 1,
        "fertilizer_interval_days": 21
    },

    "Wheat": {
        "water_interval_days": 5,
        "fertilizer_interval_days": 25
    },

    "Maize": {
        "water_interval_days": 4,
        "fertilizer_interval_days": 21
    },

    "Banana": {
        "water_interval_days": 2,
        "fertilizer_interval_days": 20
    },

    "Sugarcane": {
        "water_interval_days": 5,
        "fertilizer_interval_days": 30
    },

    "Groundnut": {
        "water_interval_days": 4,
        "fertilizer_interval_days": 25
    },

    "Soybean": {
        "water_interval_days": 4,
        "fertilizer_interval_days": 25
    },

    "Cucumber": {
        "water_interval_days": 2,
        "fertilizer_interval_days": 14
    },

    "Eggplant": {
        "water_interval_days": 2,
        "fertilizer_interval_days": 15
    },

    "Cabbage": {
        "water_interval_days": 3,
        "fertilizer_interval_days": 20
    },

    "Cauliflower": {
        "water_interval_days": 3,
        "fertilizer_interval_days": 20
    },

    "Carrot": {
        "water_interval_days": 3,
        "fertilizer_interval_days": 21
    },

    "Garlic": {
        "water_interval_days": 4,
        "fertilizer_interval_days": 25
    },

    "Ginger": {
        "water_interval_days": 3,
        "fertilizer_interval_days": 25
    },

    "Strawberry": {
        "water_interval_days": 2,
        "fertilizer_interval_days": 14
    },

    "Apple": {
        "water_interval_days": 5,
        "fertilizer_interval_days": 30
    },

    "Grape": {
        "water_interval_days": 4,
        "fertilizer_interval_days": 30
    },

    "Peach": {
        "water_interval_days": 5,
        "fertilizer_interval_days": 30
    }
}


DEFAULT_SCHEDULE = {
    "water_interval_days": 3,
    "fertilizer_interval_days": 21
}


# ============================================================
# GET CARE SCHEDULE
# ============================================================

def get_care_schedule(
    plant: str,
    rainfall: float = 0,
    humidity: float = 0
):

    today = datetime.now()

    # Normalize plant name
    plant_name = plant.replace("_", " ").strip().title()

    schedule = CARE_SCHEDULES.get(
        plant_name,
        DEFAULT_SCHEDULE
    )

    water_interval = schedule["water_interval_days"]
    fertilizer_interval = schedule["fertilizer_interval_days"]

    weather_adjusted = False

    # --------------------------------------------------------
    # SIMPLE WEATHER ADJUSTMENT
    # --------------------------------------------------------

    # Recent/heavy rainfall -> delay watering
    if rainfall >= 5:
        water_interval += 2
        weather_adjusted = True

    # Very humid conditions -> slightly delay watering
    elif humidity >= 85:
        water_interval += 1
        weather_adjusted = True


    # --------------------------------------------------------
    # CALCULATE NEXT DATES
    # --------------------------------------------------------

    next_watering = today + timedelta(
        days=water_interval
    )

    next_fertilizer = today + timedelta(
        days=fertilizer_interval
    )


    # --------------------------------------------------------
    # RESPONSE
    # --------------------------------------------------------

    return {
        "plant": plant_name,

        "watering_interval_days": water_interval,

        "next_watering_date":
            next_watering.strftime("%Y-%m-%d"),

        "fertilizer_interval_days":
            fertilizer_interval,

        "next_fertilizer_date":
            next_fertilizer.strftime("%Y-%m-%d"),

        "weather_adjusted":
            weather_adjusted,

        "note": (
            "Schedule is a general recommendation. "
            "Actual watering and fertilizer needs depend on "
            "soil, crop stage, local weather and field conditions."
        )
    }