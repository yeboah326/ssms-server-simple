from flask import Blueprint
from api.student.models import Student

student = Blueprint("student", __name__, url_prefix="/api/student")

@student.route("/hello")
def student_hello():
    return {"message":"Student blueprint working"}
