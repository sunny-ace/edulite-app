from fastapi import APIRouter, HTTPException
from typing import List
from schemas.course import Course

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)

# In-memory database (temporary store)
courses_db: List[Course] = []


@router.post("/", response_model=Course, status_code=201)
def create_course(course: Course):
    """
    Create a new course.
    Ensures no duplicate course ID is added.
    """
    if any(c.id == course.id for c in courses_db):
        raise HTTPException(status_code=400, detail="Course ID already exists")

    courses_db.append(course)
    return course


@router.get("/{course_id}", response_model=Course)
def get_course(course_id: int):
    """
    Retrieve a course by its ID.
    """
    for course in courses_db:
        if course.id == course_id:
            return course
    raise HTTPException(status_code=404, detail="Course not found")


@router.patch("/{course_id}/close", response_model=Course)
def close_course(course_id: int):
    """
    Mark a course as closed (is_open = False).
    """
    for course in courses_db:
        if course.id == course_id:
            course.is_open = False
            return course
    raise HTTPException(status_code=404, detail="Course not found")
