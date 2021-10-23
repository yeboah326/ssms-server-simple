from api.auth.models import SchoolUser, SuperUser
from api.tests.utils import db_reset

def test_auth_create_new_token():
    assert 1 == 1

def test_create_new_user_account(client):
    db_reset()

    reponse = client.post(
        "/register",
        json={
            "name":"Dummy User",
            "username": "dummy_u",
            "password": "123456",
            "email": "dummy@dmail.com",
            "user_type": "super_user"
        }    
    )

    user = SuperUser.find_by_username("dummy_u")

    assert user.name == "Dummy User"
    assert user.user_name == "dummy_u"
    assert user.email == "dummy@dmail.com"

def test_auth_create_super_user(app, client):
    db_reset()

    # Send request to create super_user
    reponse = client.post(
        "/api/auth/register",
        json={
            "name":"Super User",
            "username": "super_u",
            "password": "123456",
            "email": "super_u@user.com",
            "user_type": "super_user"
        }    
    )

    user = SuperUser.find_by_username("super_u")

    assert user.email == "super_u@user.com"


def test_auth_create_admin(client):
    db_reset()

    # Send request to create admin for school
    reponse = client.post(
        "/register",
        json={
            "name":"Admin User",
            "username": "admin_u",
            "password": "123456",
            "email": "admin_u@user.com",
            "school_id": "",
            "user_type": "admin"
        }    
    )

    user = SchoolUser.find_by_username("admin_u")

    assert user.email == "admin_u@user.com"

def test_auth_create_auditor(client):
    db_reset()

    # Send request to create an auditor account for school
    reponse = client.post(
        "/register",
        json={
            "name":"Auditor User",
            "username": "auditor_u",
            "password": "123456",
            "email": "auditor_u@user.com",
            "school_id": "",
            "user_type": "auditor"
        }    
    )

    user = SchoolUser.find_by_username("auditor_u")

    assert user.email == "audito_u@user.com"


def test_auth_create_teacher(client):
    db_reset()

    # Send request to create a teacher account for school
    reponse = client.post(
        "/register",
        json={
            "name":"Teacher User",
            "username": "teacher_u",
            "password": "123456",
            "email": "teacher_u@user.com",
            "school_id": "",
            "user_type": "teacher"
        }    
    )

    user = SchoolUser.find_by_username("teacher_u")

    assert user.email == "teacher_u@user.com"
