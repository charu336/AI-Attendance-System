from fastapi import FastAPI
from contextlib import asynccontextmanager
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from .models import User, Course, Attendance
from .routes import auth, courses, attendance
import os
from dotenv import load_dotenv

load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    client = AsyncIOMotorClient(os.getenv("MONGODB_URL", "mongodb://localhost:27017"))
    await init_beanie(database=client.ai_attendance_db, document_models=[User, Course, Attendance])
    yield
    # Shutdown
    client.close()

app = FastAPI(title="AI Attendance System API", version="2.0", lifespan=lifespan)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(courses.router, prefix="/courses", tags=["Courses"])
app.include_router(attendance.router, prefix="/attendance", tags=["Attendance"])

@app.get("/")
async def root():
    return {"message": "Welcome to AI Attendance System API v2"}
