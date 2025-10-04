from datetime import date
from schemas.enrollment import Enrollment, EnrollmentCreate

enrollments = []
enrollment_id_counter = 1

def enroll_user(enrollment: EnrollmentCreate) -> Enrollment:
    global enrollment_id_counter

    # ensure user is not already enrolled
    for e in enrollments:
        if e.user_id == enrollment.user_id and e.course_id == enrollment.course_id:
            return None  # already enrolled

    new_enrollment = Enrollment(
        id=enrollment_id_counter,
        user_id=enrollment.user_id,
        course_id=enrollment.course_id,
        completed=False,
    )
    enrollments.append(new_enrollment)
    enrollment_id_counter += 1
    return new_enrollment

def get_enrollments() -> list[Enrollment]:
    return enrollments

def mark_completed(enrollment_id: int) -> bool:
    for e in enrollments:
        if e.id == enrollment_id:
            e.completed = True
            return True
    return False
