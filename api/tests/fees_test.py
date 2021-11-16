from api.tests.utils_test import (
    create_academic_year,
    create_class,
    create_fee,
    create_owner,
    create_school,
    create_student,
    create_super_user,
    create_teacher,
    db_reset,
)
from api.fees.models import Fees
from datetime import datetime


def test_fees_hello(app, client):
    response = client.get("api/fees/hello")

    assert response.status_code == 200
    assert response.json["message"] == "Fees blueprint working"


# ------------------------------------------------------------------

# ---------------------------------------#
# ENDPOINT: fees_create_new_payment      #
# ---------------------------------------#
def test_fees_create_new_payment(app, client):
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

    # Create student
    student = create_student(client, owner, school_class)

    response = client.post(
        f"api/fees/student/{student.id}",
        json={"amount": 120.00},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    fee = Fees.query.filter_by(amount=120.00, student_id=student.id).first()

    assert response.status_code == 200
    assert response.json["message"] == "Fee payment created successfully"
    assert fee != None


def test_fees_create_new_payment_unathorized(app, client):
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

    # Create student
    student = create_student(client, super_user, school_class)

    response = client.post(
        f"api/fees/student/{student.id}",
        json={"amount": 120.00},
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    fee = Fees.query.filter_by(amount=120.00, student_id=student.id).first()

    assert response.status_code == 401
    assert response.json["message"] == "User is not authorized to create fee payment"
    assert fee == None


def test_fees_check_fee_payments(app, client):
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

    # Create student
    student = create_student(client, owner, school_class)

    # Make three fee payments
    for i in range(3):
        create_fee(client, owner, student)

    assert student.fees_paid_in_full == True


# ------------------------------------------------------------------

# ---------------------------------------#
# ENDPOINT: fees_modify_payment_by_id    #
# ---------------------------------------#
def test_fees_modify_payment_by_id(app, client):
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

    # Create student
    student = create_student(client, owner, school_class)

    # Create fee payment
    fee = create_fee(client, owner, student)

    response = client.put(
        f"api/fees/{fee.id}",
        json={"new_amount": 800.00},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    new_fee = Fees.find_by_fee_by_id(fee.id)

    assert response.status_code == 200
    assert response.json["message"] == "Fee payment updated successfully"
    assert new_fee.amount == 800.0


def test_fees_modify_payment_by_id_unathorized(app, client):
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

    # Create student
    student = create_student(client, super_user, school_class)

    # Create fee payment
    fee = create_fee(client, super_user, student)

    response = client.put(
        f"api/fees/{fee.id}",
        json={"new_amount": 800.00},
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    new_fee = Fees.find_by_fee_by_id(fee.id)

    assert response.status_code == 401
    assert response.json["message"] == "User is not authorized to modify fee payment"
    assert new_fee.amount != 800.0


def test_fees_modify_payment_by_id_non_existent(app, client):
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

    # Create student
    student = create_student(client, owner, school_class)

    # Create fee payment
    fee = create_fee(client, owner, student)

    response = client.put(
        f"api/fees/{fee.id + 1}",
        json={"new_amount": 800.00},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Fee payment not found"


# ------------------------------------------------------------------

# ---------------------------------------#
# ENDPOINT: fees_delete_payment_by_id    #
# ---------------------------------------#
def test_fees_delete_payment_by_id(app, client):
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

    # Create student
    student = create_student(client, owner, school_class)

    # Create fee payment
    fee = create_fee(client, owner, student)

    response = client.delete(
        f"api/fees/{fee.id}", headers={"Authorization": f"Bearer {owner['token']}"}
    )

    new_fee = Fees.find_by_fee_by_id(fee.id)

    assert response.status_code == 200
    assert response.json["message"] == "Fee payment deleted successfully"
    assert new_fee == None


def test_fees_delete_payment_by_id_unathorized(app, client):
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

    # Create student
    student = create_student(client, super_user, school_class)

    # Create fee payment
    fee = create_fee(client, super_user, student)

    response = client.delete(
        f"api/fees/{fee.id}", headers={"Authorization": f"Bearer {teacher['token']}"}
    )

    new_fee = Fees.find_by_fee_by_id(fee.id)

    assert response.status_code == 401
    assert response.json["message"] == "User is not authorized to delete fee payment"
    assert new_fee != None


def test_fees_delete_payment_by_id_non_existent(app, client):
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

    # Create student
    student = create_student(client, owner, school_class)

    # Create fee payment
    fee = create_fee(client, owner, student)

    response = client.delete(
        f"api/fees/{fee.id + 1}", headers={"Authorization": f"Bearer {owner['token']}"}
    )

    assert response.status_code == 404
    assert response.json["message"] == "Fee payment not found"


# ------------------------------------------------------------------

# ---------------------------------------#
# ENDPOINT: fees_modify_payment_by_id    #
# ---------------------------------------#
def test_fees_get_all_student_fee_payments(app, client):
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

    # Create student
    student = create_student(client, owner, school_class)

    # Create fee payment multiple fee payment
    for _ in range(3):
        create_fee(client, owner, student)

    response = client.get(
        f"api/fees/student/{student.id}",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    # date_of_birth = response.json["student"]["date_of_birth"]
    assert response.status_code == 200
    assert len(response.json["fees"]) == 3
    assert response.json["total_amount_paid"] == 360.0
    assert response.json["total_amount_to_be_paid"] == school_class.fees_to_be_paid
    # assert response.json["student"] == {
    #     'class_id': school_class.id,
    #     'date_of_birth': datetime(date_of_birth.year, date_of_birth.month, date_of_birth.day),
    #     'fees_paid_in_full': True,
    #     'id': student.id,
    #     'name': student.name
    # }


def test_fees_get_all_student_fee_payments_unathorized(app, client):
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

    # Create student
    student = create_student(client, super_user, school_class)

    response = client.get(
        f"api/fees/student/{student.id}",
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "User is not authorized to retrieve student fee payment"
    )


def test_fees_get_all_students_fee_payments(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    owner = create_owner(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, super_user, school)

    # Create a class
    school_class = create_class(client, super_user, academic_year, 500)

    # Create student
    student = create_student(client, super_user, school_class)

    response = client.get(
        f"api/fees/students/{school_class.id}",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 200
    assert response.json["students"]
    assert len(response.json["students"]) == 1
