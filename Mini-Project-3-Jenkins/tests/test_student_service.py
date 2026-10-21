
import pytest

from database.db import db
from app.services.student_service import StudentService


@pytest.fixture(autouse=True)
def reset_database():
    db.reset()


def test_get_existing_student():
    student = StudentService.get_student("S001")
    assert student["name"] == "Aarav Sharma"


def test_add_student():
    student = StudentService.add_student(
        "S002", "Priya Shah", "priya@example.com"
    )
    assert student["student_id"] == "S002"


def test_duplicate_student_rejected():
    with pytest.raises(ValueError, match="already exists"):
        StudentService.add_student(
            "S001", "Duplicate Student", "duplicate@example.com"
        )


def test_missing_student_rejected():
    with pytest.raises(ValueError, match="not found"):
        StudentService.get_student("S999")


def test_successful_enrollment():
    enrollment = StudentService.enroll_student(
        "S001", "C101", "Semester 3"
    )
    assert enrollment["course_id"] == "C101"


def test_duplicate_enrollment_rejected():
    StudentService.enroll_student("S001", "C101", "Semester 3")

    with pytest.raises(ValueError, match="Duplicate enrollment"):
        StudentService.enroll_student("S001", "C101", "Semester 3")


def test_marks_and_gpa_calculation():
    StudentService.enroll_student("S001", "C101", "Semester 3")
    StudentService.record_marks(
        "S001", "C101", "Semester 3", 85
    )

    assert StudentService.calculate_gpa("S001", "Semester 3") == 9.0


def test_marks_without_enrollment_rejected():
    with pytest.raises(ValueError, match="not enrolled"):
        StudentService.record_marks(
            "S001", "C101", "Semester 3", 85
        )


def test_invalid_marks_rejected():
    StudentService.enroll_student("S001", "C101", "Semester 3")

    with pytest.raises(ValueError, match="between 0 and 100"):
        StudentService.record_marks(
            "S001", "C101", "Semester 3", 120
        )


def test_semester_credit_limit():
    StudentService.add_course("C104", "Advanced AI", 8)

    StudentService.enroll_student("S001", "C101", "Semester 3")
    StudentService.enroll_student("S001", "C102", "Semester 3")
    StudentService.enroll_student("S001", "C103", "Semester 3")

    with pytest.raises(ValueError, match="credit limit"):
        StudentService.enroll_student("S001", "C104", "Semester 3")
