
import pytest

from app import create_app
from database.db import db


@pytest.fixture()
def client():
    db.reset()
    app = create_app()
    app.config["TESTING"] = True

    with app.test_client() as test_client:
        yield test_client


def test_health_endpoint(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"


def test_get_existing_student(client):
    response = client.get("/api/students/S001")

    assert response.status_code == 200
    assert response.json["name"] == "Aarav Sharma"


def test_missing_student_returns_404(client):
    response = client.get("/api/students/S999")

    assert response.status_code == 404
    assert "error" in response.json


def test_create_student_endpoint(client):
    response = client.post(
        "/api/students",
        json={
            "student_id": "S002",
            "name": "Priya Shah",
            "email": "priya@example.com",
        },
    )

    assert response.status_code == 201
    assert response.json["student_id"] == "S002"


def test_enroll_student_endpoint(client):
    response = client.post(
        "/api/enrollments",
        json={
            "student_id": "S001",
            "course_id": "C101",
            "semester": "Semester 3",
        },
    )

    assert response.status_code == 201
    assert response.json["course_id"] == "C101"


def test_record_marks_endpoint(client):
    client.post(
        "/api/enrollments",
        json={
            "student_id": "S001",
            "course_id": "C101",
            "semester": "Semester 3",
        },
    )

    response = client.post(
        "/api/marks",
        json={
            "student_id": "S001",
            "course_id": "C101",
            "semester": "Semester 3",
            "marks": 85,
        },
    )

    assert response.status_code == 201
    assert response.json["marks"] == 85.0


def test_gpa_endpoint(client):
    client.post(
        "/api/enrollments",
        json={
            "student_id": "S001",
            "course_id": "C101",
            "semester": "Semester 3",
        },
    )
    client.post(
        "/api/marks",
        json={
            "student_id": "S001",
            "course_id": "C101",
            "semester": "Semester 3",
            "marks": 85,
        },
    )

    response = client.get(
        "/api/students/S001/gpa/Semester%203"
    )

    assert response.status_code == 200
    assert response.json["gpa"] == 9.0
