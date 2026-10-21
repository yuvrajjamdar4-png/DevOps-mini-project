
from database.db import db


class StudentService:
    """Business logic for students, enrollment, and academic marks."""

    @staticmethod
    def add_student(student_id, name, email):
        if not all(
            isinstance(value, str) and value.strip()
            for value in (student_id, name, email)
        ):
            raise ValueError("Student ID, name and email are required.")

        if student_id in db.students:
            raise ValueError("Student already exists.")

        if "@" not in email:
            raise ValueError("A valid email address is required.")

        student = {
            "student_id": student_id,
            "name": name.strip(),
            "email": email.strip(),
        }
        db.students[student_id] = student
        return student

    @staticmethod
    def get_student(student_id):
        student = db.students.get(student_id)
        if student is None:
            raise ValueError("Student not found.")
        return student

    @staticmethod
    def add_course(course_id, name, credits):
        if course_id in db.courses:
            raise ValueError("Course already exists.")

        if not isinstance(credits, int) or credits <= 0:
            raise ValueError("Credits must be a positive integer.")

        course = {
            "course_id": course_id,
            "name": name,
            "credits": credits,
        }
        db.courses[course_id] = course
        return course

    @staticmethod
    def enroll_student(student_id, course_id, semester):
        StudentService.get_student(student_id)

        if course_id not in db.courses:
            raise ValueError("Course not found.")

        if not semester or not semester.strip():
            raise ValueError("Semester is required.")

        for enrollment in db.enrollments:
            if (
                enrollment["student_id"] == student_id
                and enrollment["course_id"] == course_id
                and enrollment["semester"] == semester
            ):
                raise ValueError("Duplicate enrollment.")

        current_credits = sum(
            db.courses[item["course_id"]]["credits"]
            for item in db.enrollments
            if item["student_id"] == student_id
            and item["semester"] == semester
        )

        course_credits = db.courses[course_id]["credits"]
        if current_credits + course_credits > 18:
            raise ValueError("Semester credit limit of 18 exceeded.")

        enrollment = {
            "student_id": student_id,
            "course_id": course_id,
            "semester": semester,
        }
        db.enrollments.append(enrollment)
        return enrollment

    @staticmethod
    def record_marks(student_id, course_id, semester, marks):
        StudentService.get_student(student_id)

        if not any(
            item["student_id"] == student_id
            and item["course_id"] == course_id
            and item["semester"] == semester
            for item in db.enrollments
        ):
            raise ValueError("Student is not enrolled in this course.")

        if (
            isinstance(marks, bool)
            or not isinstance(marks, (int, float))
            or not 0 <= marks <= 100
        ):
            raise ValueError("Marks must be between 0 and 100.")

        key = (student_id, course_id, semester)
        db.marks[key] = float(marks)
        return {
            "student_id": student_id,
            "course_id": course_id,
            "semester": semester,
            "marks": float(marks),
        }

    @staticmethod
    def calculate_gpa(student_id, semester):
        StudentService.get_student(student_id)

        grade_points = {
            "O": 10,
            "A+": 9,
            "A": 8,
            "B+": 7,
            "B": 6,
            "C": 5,
            "D": 4,
            "F": 0,
        }

        earned_points = 0
        total_credits = 0

        for enrollment in db.enrollments:
            if (
                enrollment["student_id"] != student_id
                or enrollment["semester"] != semester
            ):
                continue

            key = (
                student_id,
                enrollment["course_id"],
                semester,
            )
            if key not in db.marks:
                continue

            marks = db.marks[key]
            if marks >= 90:
                grade = "O"
            elif marks >= 80:
                grade = "A+"
            elif marks >= 70:
                grade = "A"
            elif marks >= 60:
                grade = "B+"
            elif marks >= 50:
                grade = "B"
            elif marks >= 40:
                grade = "C"
            elif marks >= 35:
                grade = "D"
            else:
                grade = "F"

            credits = db.courses[enrollment["course_id"]]["credits"]
            earned_points += grade_points[grade] * credits
            total_credits += credits

        if total_credits == 0:
            raise ValueError("No graded courses found for this semester.")

        return round(earned_points / total_credits, 2)
