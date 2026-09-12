from fastapi import APIRouter, HTTPException
from datetime import datetime


router = APIRouter(
    prefix="/api/market",
    tags=["Market Price"]
)


# ============================================================
# SAMPLE MARKET DATA
# Development data only.
# Replace/connect with a live market data source later.
# ============================================================

MARKET_PRICES = {
    "Rice": {
        "unit": "quintal",
        "min_price": 2200,
        "max_price": 2800,
        "modal_price": 2500
    },

    "Wheat": {
        "unit": "quintal",
        "min_price": 2300,
        "max_price": 2900,
        "modal_price": 2600
    },

    "Maize": {
        "unit": "quintal",
        "min_price": 1900,
        "max_price": 2400,
        "modal_price": 2150
    },

    "Tomato": {
        "unit": "quintal",
        "min_price": 1800,
        "max_price": 3200,
        "modal_price": 2500
    },

    "Potato": {
        "unit": "quintal",
        "min_price": 1600,
        "max_price": 2400,
        "modal_price": 2000
    },

    "Groundnut": {
        "unit": "quintal",
        "min_price": 5500,
        "max_price": 7000,
        "modal_price": 6250
    },

    "Sugarcane": {
        "unit": "quintal",
        "min_price": 300,
        "max_price": 400,
        "modal_price": 350
    }
}


# ============================================================
# GET ALL AVAILABLE PRICES
# ============================================================

@router.get("/prices")
def get_all_market_prices():

    return {
        "status": "success",
        "data_type": "development_sample",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_crops": len(MARKET_PRICES),
        "prices": MARKET_PRICES,
        "note": (
            "These are development sample values and must not be "
            "treated as live market prices."
        )
    }


# ============================================================
# GET PRICE FOR ONE CROP
# ============================================================

@router.get("/price/{crop_name}")
def get_crop_market_price(crop_name: str):

    crop = crop_name.strip().title()

    price = MARKET_PRICES.get(crop)

    if price is None:
        raise HTTPException(
            status_code=404,
            detail="Market price information not available for this crop."
        )

    return {
        "status": "success",
        "data_type": "development_sample",
        "crop": crop,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "price": price,
        "note": (
            "This is sample development data, not a live mandi price."
        )
    }


# ============================================================
# SERVICE STATUS
# ============================================================

@router.get("/")
def market_service_status():

    return {
        "status": "running",
        "service": "CareBloom Market Price Service"
    }