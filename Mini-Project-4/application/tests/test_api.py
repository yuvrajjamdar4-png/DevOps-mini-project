from run import app


def test_health_endpoint():
    client = app.test_client()
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy"}


def test_list_students_endpoint():
    client = app.test_client()
    response = client.get("/api/students")

    assert response.status_code == 200
    assert isinstance(response.get_json(), list)


def test_add_student_endpoint():
    client = app.test_client()
    response = client.post(
        "/api/students",
        json={
            "student_id": "TEST999",
            "name": "Test Student",
            "email": "test999@example.com",
        },
    )

    assert response.status_code == 201
    assert response.get_json()["student_id"] == "TEST999"
