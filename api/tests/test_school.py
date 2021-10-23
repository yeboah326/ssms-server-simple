from api.school.models import School
from api.tests.utils import create_school, db_reset

def test_school_hello(app, client):
    response = client.get("api/school/hello")

    assert response.status_code == 200

#---------------------------------#
# Endpoint: school_create         #
#---------------------------------#
def test_school_create_successful(app, client):
    db_reset()

    response = client.post(
        "api/school/create",
        json={
            "name": "Rachael Shilo School Complex",
            "location": "Accra"
        }
    )

    school = School.find_by_name("Rachael Shilo School Complex")

    assert response.status_code == 200
    assert response.json["message"] == f"{school.name} created successfully"

def test_create_school_already_exists(app, client):
    create_school()

    response = client.post(
        "api/school/create",
        json={
            "name": "Rachael Shilo School Complex",
            "location": "Accra"
        }
    )

    assert response.status_code == 401
    assert response["message"] == "A school with that name already exists"

#--------------------------------------------------------------------


#---------------------------------#
# Endpoint: school_modify_by_id   #
#---------------------------------#
def test_school_modify_by_id_does_not_exist(app, client):
    db_reset()

    response = client.post(
        "api/school/modify",
        json={
            "id": "1",
            "new_name": "AME Zion JHS",
            "new_location": "Tarkwa"
        }
    )

    assert response.status_code == 401
    assert response.json["message"] == "A school with the given ID does not exist"

def test_school_modify_by_id_new_name_already_exists(app, client):
    db_reset()

    created_school = create_school()

    response = client.post(
        "api/school/modify",
        json={
            "id": f"{created_school.id}",
            "new_name": "Rachael Shilo School Complex",
            "new_location": "Tarkwa"
        }
    )

    assert response.status_code == 401
    assert response.json["message"] == "A school with that name already exists"


def test_school_modify_by_id_successful(app,client):
    db_reset()

    created_school = create_school()

    response = client.post(
        "api/school/modify",
        json={
            "id": f"{create_school.id}",
            "new_name": "Akropong School For Disabilities",
            "new_location": "Akropong"
        }
    )

    assert response.status_code == 200
    assert response.json["message"] == "School updated successfully"

#--------------------------------------------------------------------

#---------------------------------#
# Endpoint: school_delete_by_id   #
#---------------------------------#
def test_school_delete_by_id_does_not_exist(app, client):
    db_reset()

    response = client.post(
        "api/school/delete",
        json={
            "id":"1",
        }
    )

    assert response.status_code == 401
    assert response.json["message"] == "A school with the given ID does not exist"

def test_school_delete_by_id_successful(app,client):
    db_reset()

    created_school = create_school()

    response = client.post(
        "api/school/delete",
        json={
            "id":f"{created_school}"
        }
    )

    assert response.status_code == 200
    assert response.json["School deleted successfuly"]
#--------------------------------------------------------------------
