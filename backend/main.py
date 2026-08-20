from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.consultation import router as consultation_router
from backend.routes.disease import router as disease_router
from backend.routes.auth import router as auth_router
from backend.routes.plants import router as plants_router
from backend.routes.reminders import router as reminders_router

from database.database import create_tables


# Create FastAPI application FIRST
app = FastAPI(
    title="CareBloom API",
    description="AI-powered multi-crop leaf disease detection and care assistant",
    version="1.0.0"
)


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect all API routes
app.include_router(disease_router)
app.include_router(auth_router)
app.include_router(plants_router)
app.include_router(reminders_router)
app.include_router(consultation_router)




# Create database tables when backend starts
@app.on_event("startup")
def startup_event():
    create_tables()


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to CareBloom Backend",
        "status": "running"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }