# main.py
from fastapi import FastAPI
from app.database.database import engine
from app.models.user_model import Base
from app.api.v1.endpoints import auth, weather  # Import routers

# Initialize FastAPI app
app = FastAPI()

# Create database tables at startup
@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(bind=engine)

# Include routers for each module
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(weather.router, prefix="/api/v1/weather")
