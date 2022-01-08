from api.auth.models import SuperUser
from api.expenditure.models import Expenditure, ExpenditureType
from api.tests.utils_test import (
    create_academic_year,
    create_expenditure,
    create_owner,
    create_super_user,
    create_teacher,
    create_school,
    db_reset,
)
import datetime


def test_expenditure_hello(app, client):
    response = client.get("api/expenditure/hello")

    assert response.status_code == 200
    assert response.json["message"] == "Expenditure blueprint working"


# ------------------------------------------------------------------

# -----------------------------------#
# ENDPOINT: expenditure_create_new   #
# -----------------------------------#
def test_get_all_expenditure_types(app, client):
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

    response = client.get(
        f"/api/expenditure/academic_year/{academic_year.id}/types",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 200
    assert response.json["expenditure_types"]
    assert len(response.json["expenditure_types"]) == 6


def test_get_all_expenditure_types_unauthorized(app, client):
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

    # Create new teacher
    teacher = create_teacher(client, school_id=school.id)

    response = client.get(
        f"/api/expenditure/academic_year/{academic_year.id}/types",
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert response.json["message"] == "User is not authorized to create expenditure"



# -----------------------------------#
# ENDPOINT: expenditure_create_new   #
# -----------------------------------#
def test_expenditure_create_new(app, client):
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

    # Get expenditure type
    expenditure_type = ExpenditureType.find_by_academic_year_id(academic_year.id)[0]

    response = client.post(
        f"api/expenditure/expenditure_type/{expenditure_type.id}",
        json={"description": "Bought some boxes of chalk", "amount": 500.00},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    expenditure = Expenditure.query.filter_by(
        description="Bought some boxes of chalk", amount=500.00
    ).first()

    assert response.status_code == 200
    assert response.json["message"] == "Expenditure created successfully"
    assert expenditure != None


def test_expenditure_create_new_unauthorized(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new teacher
    teacher = create_teacher(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, super_user, school)

    # Get expenditure type
    expenditure_type = ExpenditureType.find_by_academic_year_id(academic_year.id)[0]


    response = client.post(
        f"api/expenditure/expenditure_type/{expenditure_type.id}",
        json={"description": "Bought some boxes of chalk", "amount": 500.00},
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    expenditure = Expenditure.query.filter_by(
        description="Bought some boxes of chalk", amount=500.00
    ).first()

    assert response.status_code == 401
    assert response.json["message"] == "User is not authorized to create expenditure"
    assert expenditure == None


# ------------------------------------------------------------------

# -------------------------------------#
# ENDPOINT: expenditure_modify_by_id   #
# -------------------------------------#
def test_expenditure_modify_by_id(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new teacher
    owner = create_owner(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, owner, school)

    # Create expenditure
    expenditure = create_expenditure(client, owner, academic_year)

    response = client.put(
        f"api/expenditure/{expenditure.id}",
        json={"new_description": "Bought boxes of markers", "new_amount": 650.00},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    new_expenditure = Expenditure.find_by_id(expenditure.id)

    assert response.status_code == 200
    assert response.json["message"] == "Expenditure updated successfully"
    assert new_expenditure.description == "Bought boxes of markers"
    assert new_expenditure.amount == 650.00


def test_expenditure_modify_by_id_non_existent(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new teacher
    owner = create_owner(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, owner, school)

    # Create expenditure
    expenditure = create_expenditure(client, owner, academic_year)

    response = client.put(
        f"api/expenditure/{expenditure.id + 1}",
        json={"new_description": "Bought boxes of markers", "new_amount": 650.00},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Expenditure not found"


def test_expenditure_modify_by_id_unauthorized(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new teacher
    teacher = create_teacher(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, super_user, school)

    # Create expenditure
    expenditure = create_expenditure(client, super_user, academic_year)

    response = client.put(
        f"api/expenditure/{expenditure.id}",
        json={"new_description": "Bought boxes of markers", "new_amount": 650.00},
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    new_expenditure = Expenditure.find_by_id(expenditure.id)

    assert response.status_code == 401
    assert response.json["message"] == "User is not authorized to modify expenditure"
    assert new_expenditure.description != "Bought boxes of markers"
    assert new_expenditure.amount != 650.00


# ------------------------------------------------------------------

# -------------------------------------#
# ENDPOINT: expenditure_delete_by_id   #
# -------------------------------------#
def test_expenditure_delete_by_id(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new teacher
    owner = create_owner(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, owner, school)

    # Create expenditure
    expenditure = create_expenditure(client, owner, academic_year)

    response = client.delete(
        f"api/expenditure/{expenditure.id}",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    new_expenditure = Expenditure.find_by_id(expenditure.id)

    assert response.status_code == 200
    assert response.json["message"] == "Expenditure deleted successfully"
    assert new_expenditure == None


def test_expenditure_delete_by_id_non_existent(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new teacher
    owner = create_owner(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, owner, school)

    # Create expenditure
    expenditure = create_expenditure(client, owner, academic_year)

    response = client.delete(
        f"api/expenditure/{expenditure.id + 1}",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Expenditure not found"


def test_expenditure_delete_by_id_unauthorized(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new teacher
    teacher = create_teacher(client, school_id=school.id)

    # Create an academic year
    academic_year = create_academic_year(client, super_user, school)

    # Create expenditure
    expenditure = create_expenditure(client, super_user, academic_year)

    response = client.delete(
        f"api/expenditure/{expenditure.id}",
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    new_expenditure = Expenditure.find_by_id(expenditure.id)

    assert response.status_code == 401
    assert response.json["message"] == "User is not authorized to delete an expenditure"


# ------------------------------------------------------------------

# --------------------------------------------------#
# ENDPOINT: expenditure_get_all_for_academic_year   #
# --------------------------------------------------#
def test_expenditure_get_all_by_expenditure_type_id(app, client):
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

    # Create expenditure
    expenditure = create_expenditure(client, owner, academic_year)

    # Get expenditure type
    expenditure_type = ExpenditureType.find_by_academic_year_id(academic_year.id)[0]

    response = client.get(
        f"api/expenditure/expenditure_type/{expenditure_type.id}?month=13",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 200
    assert response.json["expenditures"][0]["expenditure_type_id"] == expenditure_type.id
    assert response.json["expenditures"][0]["amount"] == expenditure.amount
    assert response.json["expenditures"][0]["description"] == expenditure.description
    assert response.json["expenditures"][0]["id"] == expenditure.id


# TODO: Write a better test
def test_expenditure_get_all_by_expenditure_type_id_paginate(app, client):
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

    # Create five expenditures
    for _ in range(5):
        create_expenditure(client, owner, academic_year)

    current_month = datetime.datetime.today().month

    # Get expenditure type
    expenditure_type = ExpenditureType.find_by_academic_year_id(academic_year.id)[0]

    response = client.get(
        f"api/expenditure/expenditure_type/{expenditure_type.id}?page=1&per_page=2&month={current_month}",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 200
    assert response.json["total_pages"] == 3
    assert response.json["prev_page"] == None
    assert response.json["next_page"] == 2
    assert response.json["total_expenditure"] == 2500.0


def test_expenditure_get_all_by_expenditure_type_id_unauthorized(app, client):
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

    # Create expenditure
    expenditure = create_expenditure(client, super_user, academic_year)

    # Get expenditure type
    expenditure_type = ExpenditureType.find_by_academic_year_id(academic_year.id)[0]


    response = client.get(
        f"api/expenditure/expenditure_type/{expenditure_type.id}",
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert response.json["message"] == "User is not authorized to retrieve expenditure"


# ------------------------------------------------------------------

# -------------------------------------#
# ENDPOINT: expenditure_get_by_id   #
# -------------------------------------#
def test_expenditure_get_by_id(app, client):
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

    # Create expenditure
    expenditure = create_expenditure(client, owner, academic_year)

    # Get expenditure type
    expenditure_type = ExpenditureType.find_by_academic_year_id(academic_year.id)[0]

    response = client.get(
        f"api/expenditure/{expenditure.id}",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 200
    assert response.json["expenditure"]["expenditure_type_id"] == expenditure_type.id
    assert response.json["expenditure"]["amount"] == expenditure.amount
    assert response.json["expenditure"]["description"] == expenditure.description
    assert response.json["expenditure"]["id"] == expenditure.id


def test_expenditure_get_by_id_non_existent(app, client):
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

    # Create expenditure
    expenditure = create_expenditure(client, owner, academic_year)

    response = client.get(
        f"api/expenditure/{expenditure.id + 1}",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Expenditure not found"


def test_expenditure_get_by_id_unauthorized(app, client):
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

    # Create expenditure
    expenditure = create_expenditure(client, super_user, academic_year)

    response = client.get(
        f"api/expenditure/{expenditure.id}",
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert response.json["message"] == "User is not authorized to view an expenditure"
