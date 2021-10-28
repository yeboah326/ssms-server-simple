from datetime import datetime
from api import db
from api.auth.models import SchoolUser, User, SuperUser
from api.school.models import AcademicYear, Class, School
from api.student.models import Student
from api.expenditure.models import Expenditure
from api.fees.models import Fees


def db_reset():
    """db_reset() - Drops all the data in all tables before the test runs"""
    SuperUser.query.delete()
    SchoolUser.query.delete()
    Fees.query.delete()
    Student.query.delete()
    Class.query.delete()
    Expenditure.query.delete()
    AcademicYear.query.delete()
    School.query.delete()
    User.query.delete()
    db.session.commit()


def create_school(client, super_user_token):
    """Creates an instance of school"""

    client.post(
        "api/school/create",
        json={"name": "Rachael Shilo School Complex", "location": "Accra"},
        headers={"Authorization": f"Bearer {super_user_token}"},
    )

    school = School.find_by_name("Rachael Shilo School Complex")

    return school


def create_super_user(app, client):
    # Create and store user
    client.post(
        "/api/auth/register",
        json={
            "name": "Super User",
            "username": "super_u",
            "password": "123456",
            "email": "super_u@user.com",
            "user_type": "super_user",
        },
    )

    super_user = SuperUser.find_by_email("super_u@user.com")

    # Login user to generate the token
    response = client.post(
        "api/auth/token", json={"username": "super_u", "password": "123456"}
    )

    return {"user": super_user, "token": response.json["token"]}


def create_new_admin(client, school_id):
    # Create and store user
    client.post(
        "/api/auth/register",
        json={
            "name": "Admin User",
            "username": "admin_u",
            "password": "123456",
            "email": "admin_u@user.com",
            "school_id": f"{school_id}",
            "user_type": "admin",
        },
    )

    admin = SchoolUser.find_by_email("admin_u@user.com")

    # Login user to generate the token
    response = client.post(
        "api/auth/token", json={"username": "admin_u", "password": "123456"}
    )

    return {"user": admin, "token": response.json["token"]}


def create_new_auditor(client, school_id):
    # Create the user to be stored
    reponse = client.post(
        "/api/auth/register",
        json={
            "name": "Auditor User",
            "username": "auditor_u",
            "password": "123456",
            "email": "auditor_u@user.com",
            "school_id": f"{school_id}",
            "user_type": "auditor",
        },
    )

    auditor = SchoolUser.find_by_email("auditor_u@user.com")

    # Login user to generate the token
    response = client.post(
        "api/auth/token", json={"username": "auditor_u", "password": "123456"}
    )

    return {"user": auditor, "token": response.json["token"]}


def create_teacher(client, school_id):
    # Send request to create a teacher account for school
    client.post(
        "/api/auth/register",
        json={
            "name": "Teacher User",
            "username": "teacher_u",
            "password": "123456",
            "email": "teacher_u@user.com",
            "school_id": f"{school_id}",
            "user_type": "teacher",
        },
    )

    teacher = SchoolUser.find_by_email("teacher_u@user.com")

    # Login user to generate the token
    response = client.post(
        "api/auth/token", json={"username": "teacher_u", "password": "123456"}
    )

    return {"user": teacher, "token": response.json["token"]}


def create_owner(client, school_id):
    # Send request to create a teacher account for school
    client.post(
        "/api/auth/register",
        json={
            "name": "Owner User",
            "username": "owner_u",
            "password": "123456",
            "email": "owner_u@user.com",
            "school_id": f"{school_id}",
            "user_type": "owner",
        },
    )

    owner = SchoolUser.find_by_email("owner_u@user.com")

    # Login user to generate the token
    response = client.post(
        "api/auth/token", json={"username": "owner_u", "password": "123456"}
    )

    return {"user": owner, "token": response.json["token"]}


def create_academic_year(client, user, school):
    client.post(
        "api/school/academic_year",
        json={"name": "2018/2019", "school_id": f"{school.id}"},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    academic_year = AcademicYear.query.filter_by(name="2018/2019").first()

    return academic_year


def create_class(client, user, academic_year):
    client.post(
        "api/school/class",
        json={"academic_year_id": academic_year.id, "class_name": "JHS 3"},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    school_class = Class.query.filter_by(
        name="JHS 3", academic_year_id=academic_year.id
    ).first()

    return school_class


def create_student(client, user, school_class):
    client.post(
        f"api/student/class/{school_class.id}",
        json={
            "name": "Ama Yeboah",
            "date_of_birth": datetime(2011, 1, 1),
        },
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    student = Student.query.filter_by(
        name="Ama Yeboah", date_of_birth=datetime(2011, 1, 1)
    ).first()

    return student


def create_expenditure(client, user, academic_year):
    client.post(
        f"api/expenditure/academic_year/{academic_year.id}",
        json={"description": "Bought some boxes of chalk", "amount": 500.00},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    expenditure = Expenditure.query.filter_by(
        description="Bought some boxes of chalk", amount=500.00
    ).first()

    return expenditure


def create_fee(client, user, student):
    client.post(
        f"api/fees/student/{student.id}",
        json={"amount": 120.00},
        headers={"Authorization": f"Bearer {user['token']}"},
    )

    fee = Fees.query.filter_by(amount=120.00, student_id=student.id).first()

    return fee
