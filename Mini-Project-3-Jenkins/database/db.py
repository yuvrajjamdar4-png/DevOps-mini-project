
class Database:
    """Simple in-memory data store for the academic platform."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.students = {
            "S001": {
                "student_id": "S001",
                "name": "Aarav Sharma",
                "email": "aarav@example.com",
            }
        }
        self.courses = {
            "C101": {
                "course_id": "C101",
                "name": "Python Programming",
                "credits": 4,
            },
            "C102": {
                "course_id": "C102",
                "name": "Database Systems",
                "credits": 3,
            },
            "C103": {
                "course_id": "C103",
                "name": "Machine Learning",
                "credits": 4,
            },
        }
        self.enrollments = []
        self.marks = {}


db = Database()
