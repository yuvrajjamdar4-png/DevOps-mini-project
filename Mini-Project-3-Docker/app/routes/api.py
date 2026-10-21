
from flask import Blueprint, jsonify, request

from app.services.student_service import StudentService

api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health():
    return jsonify({"status": "healthy"}), 200


@api_bp.post("/students")
def add_student():
    data = request.get_json(silent=True) or {}
    try:
        student = StudentService.add_student(
            data.get("student_id"),
            data.get("name"),
            data.get("email"),
        )
        return jsonify(student), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@api_bp.get("/students/<student_id>")
def get_student(student_id):
    try:
        return jsonify(StudentService.get_student(student_id)), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 404


@api_bp.post("/enrollments")
def enroll_student():
    data = request.get_json(silent=True) or {}
    try:
        enrollment = StudentService.enroll_student(
            data.get("student_id"),
            data.get("course_id"),
            data.get("semester"),
        )
        return jsonify(enrollment), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@api_bp.post("/marks")
def record_marks():
    data = request.get_json(silent=True) or {}
    try:
        result = StudentService.record_marks(
            data.get("student_id"),
            data.get("course_id"),
            data.get("semester"),
            data.get("marks"),
        )
        return jsonify(result), 201
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400


@api_bp.get("/students/<student_id>/gpa/<semester>")
def calculate_gpa(student_id, semester):
    try:
        gpa = StudentService.calculate_gpa(student_id, semester)
        return jsonify({
            "student_id": student_id,
            "semester": semester,
            "gpa": gpa,
        }), 200
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
