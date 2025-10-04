# tests/test_enrollments.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import app
from fastapi.testclient import TestClient


client = TestClient(app)

def test_create_and_complete_enrollment_flow():
    # 1) create user
    r = client.post("/users/", json={"name": "EnrollUser", "email": "enrolluser@example.com"})
    assert r.status_code == 200
    user = r.json()
    user_id = user["id"]

    # 2) create course (client-supplied id — keep consistent with your course route)
    r = client.post("/courses/", json={"id": 1111, "title": "Enroll Course", "description": "desc"})
    assert r.status_code == 200
    course = r.json()
    course_id = course["id"]

    # 3) enroll
    r = client.post("/enrollments/", json={"user_id": user_id, "course_id": course_id})
    assert r.status_code == 200
    enrollment = r.json()
    enrollment_id = enrollment["id"]
    assert enrollment["user_id"] == user_id
    assert enrollment["course_id"] == course_id
    assert enrollment["completed"] is False

    # 4) duplicate enroll fails
    r = client.post("/enrollments/", json={"user_id": user_id, "course_id": course_id})
    assert r.status_code == 400

    # 5) mark complete
    r = client.post(f"/enrollments/{enrollment_id}/complete")
    assert r.status_code == 200
    assert r.json()["completed"] is True

def test_cannot_enroll_inactive_user_or_closed_course():
    # create user and deactivate
    r = client.post("/users/", json={"name": "InactiveUser", "email": "inactive@example.com"})
    assert r.status_code == 200
    u = r.json()
    uid = u["id"]

    r = client.patch(f"/users/{uid}/deactivate")
    assert r.status_code == 200

    # create a course
    r = client.post("/courses/", json={"id": 2222, "title": "Closed Course", "description": "x"})
    assert r.status_code == 200
    c = r.json()
    cid = c["id"]

    # close the course
    r = client.patch(f"/courses/{cid}/close")
    assert r.status_code == 200

    # attempt to enroll inactive user (use a different course so we test user check)
    r = client.post("/courses/", json={"id": 2223, "title": "Open Course", "description": "y"})
    assert r.status_code == 200
    open_course_id = r.json()["id"]

    r = client.post("/enrollments/", json={"user_id": uid, "course_id": open_course_id})
    assert r.status_code == 400

    # attempt to enroll an active user into closed course
    r = client.post("/users/", json={"name": "ActiveUser", "email": "active@example.com"})
    assert r.status_code == 200
    active_uid = r.json()["id"]

    r = client.post("/enrollments/", json={"user_id": active_uid, "course_id": cid})
    assert r.status_code == 400
