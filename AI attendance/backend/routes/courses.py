from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from ..models import Course, User, UserRole
from ..auth import get_current_user
from pydantic import BaseModel

router = APIRouter()

class CourseCreate(BaseModel):
    name: str
    code: str
    description: str = None
    latitude: float
    longitude: float
    radius_meters: float = 100.0

@router.post("/", response_model=Course)
async def create_course(
    course_in: CourseCreate,
    current_user: User = Depends(get_current_user)
):
    if current_user.role != UserRole.TEACHER and current_user.role != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Only teachers can create courses")
    
    course = Course(
        **course_in.dict(),
        teacher=current_user
    )
    await course.insert()
    return course

@router.get("/", response_model=List[Course])
async def list_courses():
    return await Course.find_all().to_list()

@router.get("/{course_id}", response_model=Course)
async def get_course(course_id: str):
    from bson import ObjectId
    try:
        oid = ObjectId(course_id)
    except:
        raise HTTPException(status_code=400, detail="Invalid ID format")
        
    course = await Course.get(oid)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course
