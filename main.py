from fastapi import FastAPI

app = FastAPI(
    title="Mentor-Mentee IVR Backend",
    description="Backend API for the Mentor-Mentee telephone IVR",
    version="1.0.0"
)

# Temporary student data for testing
students = {
    "STU001": {
        "name": "Rahul",
        "progress": "Good",
        "attendance": 92
    },
    "STU002": {
        "name": "Ananya",
        "progress": "Excellent",
        "attendance": 96
    }
}


@app.get("/")
def home():
    return {
        "message": "Mentor-Mentee IVR Backend is running!"
    }


@app.get("/students/{student_id}/progress")
def get_progress(student_id: str):
    student = students.get(student_id)

    if not student:
        return {"error": "Student not found"}

    return {
        "student_id": student_id,
        "name": student["name"],
        "progress": student["progress"]
    }


@app.get("/students/{student_id}/attendance")
def get_attendance(student_id: str):
    student = students.get(student_id)

    if not student:
        return {"error": "Student not found"}

    return {
        "student_id": student_id,
        "name": student["name"],
        "attendance_percentage": student["attendance"]
    }


@app.post("/mentor/request/{student_id}")
def request_mentor(student_id: str):
    student = students.get(student_id)

    if not student:
        return {"error": "Student not found"}

    return {
        "message": "Mentor interaction request received",
        "student_id": student_id,
        "student_name": student["name"],
        "status": "Request submitted"
    }
