from api.school.models import AcademicYear, School, Class
from api.tests.utils_test import (
    create_owner,
    create_super_user,
    create_teacher,
    create_academic_year,
    create_school,
    create_class,
    db_reset,
)

# ----------------------------#
# ENDPOINT: school_hello     #
# ----------------------------#
def test_school_hello(client):
    response = client.get("api/school/hello")

    assert response.status_code == 200


# --------------------------------------------------------------------


# ----------------------------#
# ENDPOINT: school_create    #
# ----------------------------#
def test_school_create_successful(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    response = client.post(
        "api/school/create",
        json={"name": "Rachael Shilo School Complex", "location": "Accra"},
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    school = School.find_by_name("Rachael Shilo School Complex")

    assert response.status_code == 200
    assert response.json["message"] == f"{school.name} created successfully"


def test_create_school_already_exists(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    create_school(client, super_user["token"])

    response = client.post(
        "api/school/create",
        json={"name": "Rachael Shilo School Complex", "location": "Accra"},
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    assert response.status_code == 401
    assert response.json["message"] == "A school with that name already exists"


# --------------------------------------------------------------------


# ---------------------------------#
# ENDPOINT: school_modify_by_id   #
# ---------------------------------#
def test_school_modify_by_id_does_not_exist(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    response = client.post(
        "api/school/modify",
        json={"id": "90000", "new_name": "AME Zion JHS", "new_location": "Tarkwa"},
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    assert response.status_code == 401
    assert response.json["message"] == "A school with the given ID does not exist"


def test_school_modify_by_id_new_name_already_exists(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    response = client.post(
        "api/school/modify",
        json={
            "id": f"{school.id}",
            "new_name": "Rachael Shilo School Complex",
            "new_location": "Tarkwa",
        },
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    assert response.status_code == 401
    assert response.json["message"] == "A school with that name already exists"


def test_school_modify_by_id_successful(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    response = client.post(
        "api/school/modify",
        json={
            "id": f"{school.id}",
            "new_name": "Akropong School For Disabilities",
            "new_location": "Akropong",
        },
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    school = School.find_by_id(school.id)

    assert response.status_code == 200
    assert response.json["message"] == "School updated successfully"
    assert school.name == "Akropong School For Disabilities"


# --------------------------------------------------------------------


# ---------------------------------#
# Endpoint: school_delete_by_id   #
# ---------------------------------#
def test_school_delete_by_id_does_not_exist(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    response = client.post(
        "api/school/delete",
        json={
            "id": "90000",
        },
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "A school with the given ID does not exist"


def test_school_delete_by_id_successful(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    response = client.post(
        "api/school/delete",
        json={"id": f"{school.id}"},
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "School deleted successfully"


# --------------------------------------------------------------------


# ------------------------------------------#
# ENDPOINT: school_create_academic_year    #
# ------------------------------------------#
def test_school_create_academic_year(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    owner = create_owner(client, school_id=school.id)

    response = client.post(
        "api/school/academic_year",
        json={"name": "2018/2019", "school_id": f"{school.id}"},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    academic_year = AcademicYear.query.filter_by(name="2018/2019").first()

    assert response.status_code == 200
    assert response.json["message"] == "Academic year created successfully"
    assert academic_year.name == "2018/2019"


def test_school_create_academic_year_fail(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    owner = create_teacher(client, school_id=school.id)

    response = client.post(
        "api/school/academic_year",
        json={"name": "2018/2019", "school_id": f"{school.id}"},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "User does not have the right priveleges to perform specified actions"
    )


# --------------------------------------------------------------------

# ------------------------------------------#
# ENDPOINT: school_delete_academic_year    #
# ------------------------------------------#
def test_school_delete_academic_year_successful(app, client):
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

    response = client.delete(
        "api/school/academic_year",
        json={"academic_year_id": academic_year.id},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Academic year deleted successfully"


def test_school_delete_academic_year_fail(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    owner = create_owner(client, school_id=school.id)

    response = client.delete(
        "api/school/academic_year",
        json={"academic_year_id": "1"},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Academic does not exist"


# --------------------------------------------------------------------

# ------------------------------------------#
# ENDPOINT: school_modify_academic_year    #
# ------------------------------------------#
def test_school_modify_academic_year(app, client):
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

    response = client.put(
        "api/school/academic_year",
        json={
            "academic_year_id": academic_year.id,
            "new_academic_year_name": "2019/2020",
        },
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    updated_academic_year = AcademicYear.find_by_id(academic_year_id=academic_year.id)

    assert response.status_code == 200
    assert response.json["message"] == "Academic year updated successfully"
    assert updated_academic_year.name == "2019/2020"


def test_school_modify_academic_year_not_exist(app, client):
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

    response = client.put(
        "api/school/academic_year",
        json={
            "academic_year_id": academic_year.id + 1,
            "new_academic_year_name": "2019/2020",
        },
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Academic year does not exist"


def test_school_modify_academic_year_not_authorized(app, client):
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

    response = client.put(
        "api/school/academic_year",
        json={
            "academic_year_id": academic_year.id,
            "new_academic_year_name": "2019/2020",
        },
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "User does not have the right priveleges to perform specified actions"
    )


# --------------------------------------------------------------------

# ------------------------------------------#
# ENDPOINT: school_get_all_academic_years  #
# ------------------------------------------#
def test_school_get_all_academic_years(app, client):
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
        "api/school/academic_year",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 200
    assert response.json["academic_years"] == {f"{academic_year.id}": "2018/2019"}
    assert len(response.json["academic_years"]) == 1


# --------------------------------------------------------------------

# ----------------------------------#
# ENDPOINT: school_create_class    #
# ----------------------------------#
def test_school_create_class(app, client):
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

    response = client.post(
        "api/school/class",
        json={"academic_year_id": academic_year.id, "class_name": "JHS 3"},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    school_class = Class.query.filter_by(
        name="JHS 3", academic_year_id=academic_year.id
    ).first()

    assert response.status_code == 200
    assert response.json["message"] == "Class created successfully"
    assert school_class != None


def test_school_create_class_unauthorized(app, client):
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

    response = client.post(
        "api/school/class",
        json={"academic_year_id": academic_year.id, "class_name": "JHS 3"},
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "User does not have the right priveleges to perform specified actions"
    )


# --------------------------------------------------------------------

# ------------------------------------------#
# ENDPOINT: school_delete_class            #
# ------------------------------------------#
def test_school_delete_class(app, client):
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

    response = client.delete(
        "api/school/class",
        json={"class_id": school_class.id},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    school_class = Class.query.filter_by(
        name="JHS 3", academic_year_id=academic_year.id
    ).first()

    assert response.status_code == 200
    assert response.json["message"] == "Class deleted successfully"
    assert school_class == None


def test_school_delete_class_unauthorized(app, client):
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

    response = client.delete(
        "api/school/class",
        json={"class_id": school_class.id},
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "User does not have the right priveleges to perform specified actions"
    )


def test_school_delete_class_non_existent(app, client):
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

    response = client.delete(
        "api/school/class",
        json={"class_id": school_class.id + 1},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Class does not exist"


# --------------------------------------------------------------------

# ------------------------------------------#
# ENDPOINT: school_delete_class            #
# ------------------------------------------#
def test_school_modify_class(app, client):
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

    response = client.put(
        "api/school/class",
        json={"new_class_name": "Kindergarten 1", "class_id": school_class.id},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    school_class = Class.query.filter_by(
        name="Kindergarten 1", academic_year_id=academic_year.id
    ).first()

    assert response.status_code == 200
    assert response.json["message"] == "Class modified successfully"
    assert school_class != None


def test_school_modify_class_unauthorized(app, client):
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

    response = client.put(
        "api/school/class",
        json={"new_class_name": "Kindergarten 1", "class_id": school_class.id},
        headers={"Authorization": f"Bearer {teacher['token']}"},
    )

    assert response.status_code == 401
    assert (
        response.json["message"]
        == "User does not have the right priveleges to perform specified actions"
    )


def test_school_modify_class_non_existent(app, client):
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

    response = client.put(
        "api/school/class",
        json={"new_class_name": "Kindergarten 1", "class_id": school_class.id + 1},
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 404
    assert response.json["message"] == "Class does not exist"


# --------------------------------------------------------------------

# ------------------------------------------#
# ENDPOINT: school_get_all_class            #
# ------------------------------------------#
def test_school_get_all_class(app, client):
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

    response = client.get(
        f"api/school/academic_year/{academic_year.id}/class",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )

    assert response.status_code == 200
    assert response.json["academic_year"] == academic_year.name
    assert response.json["classes"] == {f"{school_class.id}": "JHS 3"}
