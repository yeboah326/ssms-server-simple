from datetime import datetime
from api.tests.utils_test import (
    create_student,
    db_reset,
    create_academic_year,
    create_class,
    create_super_user,
    create_owner,
    create_school,
    create_teacher,
)
from api.student.models import Student


def test_student_hello(client):
    response = client.get("api/student/hello")

    assert response.status_code == 200
    assert response.json["message"] == "Student blueprint working"


# ------------------------------------------------------------------

# -----------------------------------#
# ENDPOINT: student_create_new      #
# -----------------------------------#
def test_student_create_new(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    owner = create_owner(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, owner, school)

    # Create a class
    school_class = create_class(client, owner, academic_year)

    response = client.post(
        f"api/student/class/{school_class.id}",
        json={
            "name": "Ama Yeboah",
            "date_of_birth": datetime(2011, 1, 1),
        },
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    student = Student.query.filter_by(
        name="Ama Yeboah", date_of_birth=datetime(2011, 1, 1)
    )

    assert response.status_code == 200
    assert response.json["message"] == "Student created successfully"
    assert student != None


def test_student_create_new_unauthorized(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    owner = create_owner(client, school_id=school.id)

    # Create new teacher
    teacher = create_teacher(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, owner, school)

    # Create a class
    school_class = create_class(client, owner, academic_year)

    response = client.post(
        f"api/student/class/{school_class.id}",
        json={
            "name": "Ama Yeboah",
            "date_of_birth": datetime(2011, 1, 1),
        },
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "User does not have the right priveleges to perform specified actions"
    )


# ------------------------------------------------------------------

# -----------------------------------#
# ENDPOINT: student_modify_by_id    #
# -----------------------------------#
def test_student_modify_by_id(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    owner = create_owner(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, owner, school)

    # Create a class
    school_class = create_class(client, owner, academic_year)

    # Create a student
    student = create_student(client, owner, school_class)

    response = client.put(
        f"/api/student/{student.id}",
        json={
            "new_name": "Ama Beverly",
            "new_date_of_birth": str(datetime(2012, 1, 1)),
        },
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    new_student = Student.find_by_id(student.id)

    assert response.status_code == 200
    assert response.json["message"] == "Student updated successfully"
    assert new_student.name == "Ama Beverly"
    assert new_student.date_of_birth == datetime(2012, 1, 1, 0, 0)


def test_student_modify_by_id_non_existent(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    owner = create_owner(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, owner, school)

    # Create a class
    school_class = create_class(client, owner, academic_year)

    # Create a student
    student = create_student(client, owner, school_class)

    response = client.put(
        f"/api/student/{student.id + 1}",
        json={
            "new_name": "Ama Beverly",
            "new_date_of_birth": str(datetime(2012, 1, 1)),
        },
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Student does not exist"


def test_student_modify_by_id_unauthorized(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    teacher = create_teacher(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, super_user, school)

    # Create a class
    school_class = create_class(client, super_user, academic_year)

    # Create a student
    student = create_student(client, super_user, school_class)

    response = client.put(
        f"/api/student/{student.id}",
        json={
            "new_name": "Ama Beverly",
            "new_date_of_birth": str(datetime(2012, 1, 1)),
        },
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "User does not have the right priveleges to perform specified actions"
    )


# ------------------------------------------------------------------

# -----------------------------------#
# ENDPOINT: student_delete_by_id    #
# -----------------------------------#
def test_student_delete_by_id(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    owner = create_owner(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, owner, school)

    # Create a class
    school_class = create_class(client, owner, academic_year)

    # Create a student
    student = create_student(client, owner, school_class)

    response = client.delete(
        f"/api/student/{student.id}",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    new_student = Student.find_by_id(student.id)

    assert response.status_code == 200
    assert response.json["message"] == "Student deleted successfully"
    assert new_student == None


def test_student_delete_by_id_non_existent(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    owner = create_owner(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, owner, school)

    # Create a class
    school_class = create_class(client, owner, academic_year)

    # Create a student
    student = create_student(client, owner, school_class)

    response = client.delete(
        f"/api/student/{student.id + 1}",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Student does not exist"


def test_student_delete_by_id_unauthorized(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    teacher = create_teacher(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, super_user, school)

    # Create a class
    school_class = create_class(client, super_user, academic_year)

    # Create a student
    student = create_student(client, super_user, school_class)

    response = client.delete(
        f"/api/student/{student.id}",
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "User does not have the right priveleges to perform specified actions"
    )


# ------------------------------------------------------------------

# ------------------------------------------#
# ENDPOINT: student_get_all_by_class_id    #
# ------------------------------------------#
def test_student_get_all_by_class_id(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    owner = create_owner(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, owner, school)

    # Create a class
    school_class = create_class(client, owner, academic_year)

    # Create a student
    student = create_student(client, owner, school_class)

    response = client.get(
        f"api/student/class/{school_class.id}",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 200
    assert response.json["students"] == {f"{student.id}": f"{student.name}"}


def test_student_get_all_by_class_id_unauthorized(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    teacher = create_teacher(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, super_user, school)

    # Create a class
    school_class = create_class(client, super_user, academic_year)

    # Create a student
    student = create_student(client, super_user, school_class)

    response = client.get(
        f"api/student/class/{school_class.id}",
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "User does not have the right priveleges to perform specified actions"
    )
