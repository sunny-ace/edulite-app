from pydantic import BaseModel
from typing import Optional

# class CourseBase(BaseModel):
#     title: str
#     description: Optional[str] = None

# class CourseCreate(CourseBase):
#     pass

# class CourseUpdate(BaseModel):
#     title: Optional[str] = None
#     description: Optional[str] = None
#     is_open: Optional[bool] = None

# class Course(CourseBase):
#     id: int
#     is_open: bool = True

class Course(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_open: bool = True
