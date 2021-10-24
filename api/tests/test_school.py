from api.school.models import School
from api.tests.utils import create_new_admin, create_new_super_user, create_school, db_reset

#----------------------------#
# ENDPOINT: school_hello     #
#----------------------------#
def test_school_hello(client):
    response = client.get("api/school/hello")

    assert response.status_code == 200

#--------------------------------------------------------------------


#----------------------------#
# ENDPOINT: school_create    #
#----------------------------#
def test_school_create_successful(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_new_super_user(app,client)
        
    response = client.post(
        "api/school/create",
        json={
            "name": "Rachael Shilo School Complex",
            "location": "Accra"
        },
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    school = School.find_by_name("Rachael Shilo School Complex")

    assert response.status_code == 200
    assert response.json["message"] == f"{school.name} created successfully"

def test_create_school_already_exists(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_new_super_user(app,client)
    
    # Send request to create a new school
    create_school(app, client, super_user["token"])

    response = client.post(
        "api/school/create",
        json={
            "name": "Rachael Shilo School Complex",
            "location": "Accra"
        },
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    assert response.status_code == 401
    assert response.json["message"] == "A school with that name already exists"

#--------------------------------------------------------------------


#---------------------------------#
# ENDPOINT: school_modify_by_id   #
#---------------------------------#
def test_school_modify_by_id_does_not_exist(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_new_super_user(app,client)
    
    response = client.post(
        "api/school/modify",
        json={
            "id": "90000",
            "new_name": "AME Zion JHS",
            "new_location": "Tarkwa"
        },
        headers={"Authorization": f"Bearer {super_user['token']}"}
    )

    assert response.status_code == 401
    assert response.json["message"] == "A school with the given ID does not exist"

def test_school_modify_by_id_new_name_already_exists(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_new_super_user(app,client)
    
    # Send request to create a new school
    school = create_school(app, client, super_user["token"])
    
    response = client.post(
        "api/school/modify",
        json={
            "id": f"{school['school'].id}",
            "new_name": "Rachael Shilo School Complex",
            "new_location": "Tarkwa"
        },
        headers={"Authorization": f"Bearer {super_user['token']}"}
    )

    assert response.status_code == 401
    assert response.json["message"] == "A school with that name already exists"

def test_school_modify_by_id_successful(app,client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_new_super_user(app,client)
    
    # Send request to create a new school
    school = create_school(app, client, super_user["token"])

    response = client.post(
        "api/school/modify",
        json={
            "id": f"{school['school'].id}",
            "new_name": "Akropong School For Disabilities",
            "new_location": "Akropong"
        },
        headers={"Authorization":f"Bearer {super_user['token']}"}
    )

    assert response.status_code == 200
    assert response.json["message"] == "School updated successfully"

#--------------------------------------------------------------------


#---------------------------------#
# Endpoint: school_delete_by_id   #
#---------------------------------#
def test_school_delete_by_id_does_not_exist(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_new_super_user(app,client)
    
    response = client.post(
        "api/school/delete",
        json={
            "id":"90000",
        },
        headers={"Authorization": f"Bearer {super_user['token']}"}
    )

    assert response.status_code == 401
    assert response.json["message"] == "A school with the given ID does not exist"

def test_school_delete_by_id_successful(app,client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_new_super_user(app,client)
    
    # Send request to create a new school
    school = create_school(app, client, super_user["token"])

    response = client.post(
        "api/school/delete",
        json={
            "id":f"{school['school'].id}"
        },
        headers={"Authorization":f"Bearer {super_user['token']}"}
    )

    assert response.status_code == 200
    assert response.json["message"] == "School deleted successfully"

#--------------------------------------------------------------------
