from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
import os
import requests
from dotenv import load_dotenv

load_dotenv("backend/.env")


router = APIRouter(
    prefix="/api/market",
    tags=["Market Price"]
)


# ============================================================
# DATA.GOV.IN CONFIG
# ============================================================

DATA_GOV_API_KEY = os.getenv("DATA_GOV_API_KEY")

DATA_GOV_URL = (
    "https://api.data.gov.in/resource/"
    "9ef84268-d588-465a-a308-a864a43d0070"
)


# ============================================================
# SAMPLE FALLBACK DATA
# Used only when live API is unavailable.
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
# LIVE MARKET DATA FETCH
# ============================================================

def fetch_live_market_prices(
    commodity: str | None = None,
    state: str | None = None,
    district: str | None = None,
    limit: int = 20
):

    if not DATA_GOV_API_KEY:
        return None

    params = {
        "api-key": DATA_GOV_API_KEY,
        "format": "json",
        "limit": limit
    }

    if commodity:
        params["filters[commodity]"] = commodity.strip()

    if state:
        params["filters[state]"] = state.strip()

    if district:
        params["filters[district]"] = district.strip()

    try:
        response = requests.get(
            DATA_GOV_URL,
            params=params,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        return data.get("records", [])

    except (requests.RequestException, ValueError):
        return None


# ============================================================
# FORMAT LIVE RECORD
# ============================================================

def format_market_record(record: dict):

    return {
        "state": record.get("state"),
        "district": record.get("district"),
        "market": record.get("market"),
        "commodity": record.get("commodity"),
        "variety": record.get("variety"),
        "arrival_date": record.get("arrival_date"),
        "min_price": record.get("min_price"),
        "max_price": record.get("max_price"),
        "modal_price": record.get("modal_price"),
        "unit": "quintal"
    }


# ============================================================
# GET MARKET PRICES
# ============================================================

@router.get("/prices")
def get_all_market_prices(
    commodity: str | None = Query(default=None),
    state: str | None = Query(default=None),
    district: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100)
):

    live_records = fetch_live_market_prices(
        commodity=commodity,
        state=state,
        district=district,
        limit=limit
    )

    if live_records:

        formatted_records = [
            format_market_record(record)
            for record in live_records
        ]

        return {
            "status": "success",
            "data_type": "live_government_mandi_data",
            "source": "Open Government Data Platform India",
            "retrieved_at": datetime.now().isoformat(),
            "total_records": len(formatted_records),
            "prices": formatted_records
        }

    return {
        "status": "success",
        "data_type": "development_sample",
        "date": datetime.now().strftime("%Y-%m-%d"),
        "total_crops": len(MARKET_PRICES),
        "prices": MARKET_PRICES,
        "note": (
            "Live government mandi data is temporarily unavailable. "
            "CareBloom is showing development sample prices. "
            "These values must not be treated as live market prices."
        )
    }


# ============================================================
# GET PRICE FOR ONE CROP
# ============================================================

@router.get("/price/{crop_name}")
def get_crop_market_price(crop_name: str):

    crop = crop_name.strip().title()

    live_records = fetch_live_market_prices(
        commodity=crop,
        limit=20
    )

    if live_records:

        formatted_records = [
            format_market_record(record)
            for record in live_records
        ]

        return {
            "status": "success",
            "data_type": "live_government_mandi_data",
            "source": "Open Government Data Platform India",
            "crop": crop,
            "retrieved_at": datetime.now().isoformat(),
            "total_records": len(formatted_records),
            "prices": formatted_records
        }

    price = MARKET_PRICES.get(crop)

    if price is None:
        raise HTTPException(
            status_code=404,
            detail=(
                "Live market data is unavailable and no fallback "
                "price information exists for this crop."
            )
        )

    return {
        "status": "success",
        "data_type": "development_sample",
        "crop": crop,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "price": price,
        "note": (
            "Live government mandi data is temporarily unavailable. "
            "CareBloom is showing sample development data."
        )
    }


# ============================================================
# SERVICE STATUS
# ============================================================

@router.get("/")
def market_service_status():

    return {
        "status": "running",
        "service": "CareBloom Market Price Service",
        "live_market_provider": "Open Government Data Platform India",
        "api_key_configured": bool(DATA_GOV_API_KEY),
        "fallback_available": True
    }