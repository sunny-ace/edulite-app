from schemas.course import Course, CourseCreate, CourseUpdate

courses = []
course_id_counter = 1

def create_course(course: CourseCreate) -> Course:
    global course_id_counter
    new_course = Course(id=course_id_counter, is_open=True, **course.dict())
    courses.append(new_course)
    course_id_counter += 1
    return new_course

def get_courses() -> list[Course]:
    return courses

def get_course(course_id: int) -> Course | None:
    return next((c for c in courses if c.id == course_id), None)

def update_course(course_id: int, course_update: CourseUpdate) -> Course | None:
    course = get_course(course_id)
    if course:
        update_data = course_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(course, key, value)
        return course
    return None

def close_course(course_id: int) -> bool:
    course = get_course(course_id)
    if course:
        course.is_open = False
        return True
    return False
