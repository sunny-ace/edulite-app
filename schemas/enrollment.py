# class EnrollmentBase(BaseModel):
#     user_id: int
#     course_id: int

# class EnrollmentCreate(EnrollmentBase):
#     pass

# class Enrollment(EnrollmentBase):
#     id: int
#     completed: bool = False
from pydantic import BaseModel

class EnrollmentCreate(BaseModel):
    user_id: int
    course_id: int

class Enrollment(BaseModel):
    id: int
    user_id: int
    course_id: int
    completed: bool = False
