from fastapi import APIRouter, HTTPException
from typing import List
from schemas.enrollment import Enrollment, EnrollmentCreate
from routes.user_routes import users  # In-memory list from user_routes.py
from routes.course import courses_db  # In-memory list from course.py

router = APIRouter(
    prefix="/enrollments",
    tags=["Enrollments"]
)

# In-memory database for enrollments
enrollments_db: List[Enrollment] = []
_next_enrollment_id = 1


# Utility functions
def _find_user(user_id: int):
    """Locate a user by ID, supporting both Pydantic and dict formats."""
    for user in users:
        uid = getattr(user, "id", None) if not isinstance(user, dict) else user.get("id")
        if uid == user_id:
            return user
    return None


def _find_course(course_id: int):
    """Locate a course by ID, supporting both Pydantic and dict formats."""
    for course in courses_db:
        cid = getattr(course, "id", None) if not isinstance(course, dict) else course.get("id")
        if cid == course_id:
            return course
    return None


# Routes
@router.post("/", response_model=Enrollment, status_code=201)
def create_enrollment(payload: EnrollmentCreate):
    """
    Enroll a user in a course.
    Validates:
    - User exists and is active
    - Course exists and is open
    - User not already enrolled
    """
    global _next_enrollment_id

    user = _find_user(payload.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    is_active = getattr(user, "is_active", None) if not isinstance(user, dict) else user.get("is_active")
    if is_active is False:
        raise HTTPException(status_code=400, detail="User is not active")

    course = _find_course(payload.course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    is_open = getattr(course, "is_open", None) if not isinstance(course, dict) else course.get("is_open")
    if is_open is False:
        raise HTTPException(status_code=400, detail="Course is closed for enrollment")

    # Prevent duplicate enrollment
    for e in enrollments_db:
        if e.user_id == payload.user_id and e.course_id == payload.course_id:
            raise HTTPException(status_code=400, detail="User already enrolled in this course")

    enrollment = Enrollment(
        id=_next_enrollment_id,
        user_id=payload.user_id,
        course_id=payload.course_id,
        completed=False
    )
    enrollments_db.append(enrollment)
    _next_enrollment_id += 1

    return enrollment


@router.get("/", response_model=List[Enrollment])
def list_enrollments():
    """Return all enrollments."""
    return enrollments_db


@router.get("/{enrollment_id}", response_model=Enrollment)
def get_enrollment(enrollment_id: int):
    """Retrieve a specific enrollment by ID."""
    for e in enrollments_db:
        if e.id == enrollment_id:
            return e
    raise HTTPException(status_code=404, detail="Enrollment not found")


@router.post("/{enrollment_id}/complete", response_model=Enrollment)
def mark_complete(enrollment_id: int):
    """Mark an enrollment as completed."""
    for e in enrollments_db:
        if e.id == enrollment_id:
            e.completed = True
            return e
    raise HTTPException(status_code=404, detail="Enrollment not found")


@router.get("/user/{user_id}", response_model=List[Enrollment])
def enrollments_for_user(user_id: int):
    """Get all enrollments for a specific user."""
    if not _find_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return [e for e in enrollments_db if e.user_id == user_id]
