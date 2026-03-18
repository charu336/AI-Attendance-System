from typing import Optional, List
from beanie import Document, Link
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

class User(Document):
    email: EmailStr = Field(unique=True)
    password_hash: str
    full_name: str
    role: UserRole = UserRole.STUDENT
    # Face embedding could be stored as a list of floats
    face_embedding: Optional[List[float]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "users"

class Course(Document):
    name: str
    code: str = Field(unique=True) # e.g., CS101
    description: Optional[str] = None
    teacher: Link[User]
    # Geofence center
    latitude: float
    longitude: float
    radius_meters: float = 100.0
    schedule: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Settings:
        name = "courses"

class AttendanceStatus(str, Enum):
    PRESENT = "present"
    LATE = "late"
    ABSENT = "absent"

class Attendance(Document):
    student: Link[User]
    course: Link[Course]
    date: datetime = Field(default_factory=datetime.utcnow)
    status: AttendanceStatus = AttendanceStatus.PRESENT
    verification_method: str = "face_geofence" # or manual
    confidence_score: float = 0.0 # From face recognition
    
    class Settings:
        name = "attendance"
