from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ============================================================
# ROUTERS
# ============================================================
from backend.routes.chatbot import router as chatbot_router
from backend.routes.language import router as language_router
from backend.routes.community import router as community_router
from backend.routes.nearby_services import router as nearby_services_router
from backend.routes.market_price import router as market_price_router
from backend.routes.crop_calendar import router as crop_calendar_router
from backend.routes.schemes import router as schemes_router
from backend.routes.history import router as history_router
from backend.routes.alerts import router as alerts_router
from backend.routes.weather import router as weather_router
from backend.routes.auth import router as auth_router
from backend.routes.consultation import router as consultation_router
from backend.routes.disease import router as disease_router
from backend.routes.plants import router as plants_router
from backend.routes.reminders import router as reminders_router
from backend.routes.care import router as care_router

# ============================================================
# DATABASE
# ============================================================

from database.database import create_tables


# ============================================================
# CREATE FASTAPI APPLICATION
# ============================================================

app = FastAPI(
    title="CareBloom API",
    description=(
        "AI-powered multi-crop plant disease detection "
        "and intelligent plant care assistant"
    ),
    version="2.0.0"
)


# ============================================================
# CORS
# Allows frontend to communicate with backend
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# CONNECT ROUTERS
# ============================================================

app.include_router(auth_router)
app.include_router(disease_router)
app.include_router(plants_router)
app.include_router(reminders_router)
app.include_router(consultation_router)
app.include_router(care_router)
app.include_router(weather_router)
app.include_router(alerts_router)
app.include_router(history_router)
app.include_router(schemes_router)
app.include_router(crop_calendar_router)
app.include_router(market_price_router)
app.include_router(nearby_services_router)
app.include_router(community_router)
app.include_router(language_router)
app.include_router(chatbot_router)

# ============================================================
# DATABASE STARTUP
# ============================================================

@app.on_event("startup")
def startup_event():
    create_tables()


# ============================================================
# HOME
# ============================================================

@app.get("/", tags=["System"])
def home():
    return {
        "app": "CareBloom",
        "version": "2.0.0",
        "message": "Welcome to CareBloom Backend",
        "status": "running"
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health", tags=["System"])
def health_check():
    return {
        "status": "healthy",
        "service": "CareBloom Backend"
    }