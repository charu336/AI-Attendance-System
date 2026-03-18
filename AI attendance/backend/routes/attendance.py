from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from ..models import Attendance, Course, User, AttendanceStatus
from ..auth import get_current_user
from datetime import datetime
from geopy.distance import geodesic
import shutil
import os

router = APIRouter()

# Simple geofence check
def is_within_geofence(user_lat, user_lon, target_lat, target_lon, radius_meters):
    distance = geodesic((user_lat, user_lon), (target_lat, target_lon)).meters
    return distance <= radius_meters, distance

@router.post("/mark")
async def mark_attendance(
    course_id: str = Form(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # 1. Get Course
    from bson import ObjectId
    try:
        oid = ObjectId(course_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid Course ID")
        
    course = await Course.get(oid)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    # 2. Check Geofence
    in_geofence, distance = is_within_geofence(latitude, longitude, course.latitude, course.longitude, course.radius_meters)
    if not in_geofence:
        raise HTTPException(
            status_code=400, 
            detail=f"You are outside the class geofence. Distance: {distance:.2f}m (Max: {course.radius_meters}m)"
        )

    # 3. Check Face Pipeline (DeepFace architecture integration point)
    temp_filename = f"temp_{current_user.id}_{int(datetime.utcnow().timestamp())}.jpg"
    with open(temp_filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # Placeholder for actual DeepFace verification using temp_file and stored user embedding
    face_valid = True 
    confidence = 0.95 

    os.remove(temp_filename)

    if not face_valid:
        raise HTTPException(status_code=400, detail="Face verification failed")

    # 4. Record Attendance
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    existing = await Attendance.find_one(
        Attendance.student.id == current_user.id,
        Attendance.course.id == course.id,
        Attendance.date >= today_start
    )
    if existing:
        raise HTTPException(status_code=400, detail="Attendance already marked for today")

    attendance = Attendance(
        student=current_user,
        course=course,
        status=AttendanceStatus.PRESENT,
        verification_method="face_geofence",
        confidence_score=confidence
    )
    await attendance.insert()
    
    return {"message": "Attendance marked successfully", "distance": distance}
