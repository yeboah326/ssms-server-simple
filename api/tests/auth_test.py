from api.auth.models import SchoolUser, SuperUser
from api.tests.utils_test import (
    db_reset,
    create_school,
    create_super_user,
    create_teacher,
)


def test_auth_hello(client):
    response = client.get("api/auth/hello")

    assert response.status_code == 200
    assert response.json["message"] == "Auth blueprint is working"


def test_auth_create_super_user(client):
    db_reset()

    # Send request to create super_user
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Super User",
            "username": "super_u",
            "password": "123456",
            "email": "super_u@user.com",
            "user_type": "super_user",
        },
    )

    user = SuperUser.find_by_username("super_u")

    assert response.status_code == 200
    assert user.email == "super_u@user.com"
    assert response.json["message"] == "User created successfully"


def test_auth_create_admin(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Send request to create admin for school
    response = client.post(
        "api/auth/register",
        json={
            "name": "Admin User",
            "username": "admin_u",
            "password": "123456",
            "email": "admin_u@user.com",
            "school_id": f"{school.id}",
            "user_type": "admin",
        },
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    user = SchoolUser.find_by_username("admin_u")

    assert response.status_code == 200
    assert response.json["message"] == "User created successfully"
    assert user.email == "admin_u@user.com"


def test_auth_create_auditor(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Send request to create an auditor account for school
    response = client.post(
        "api/auth/register",
        json={
            "name": "Auditor User",
            "username": "auditor_u",
            "password": "123456",
            "email": "auditor_u@user.com",
            "school_id": f"{school.id}",
            "user_type": "auditor",
        },
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    user = SchoolUser.find_by_username("auditor_u")

    assert response.status_code == 200
    assert response.json["message"] == "User created successfully"
    assert user.email == "auditor_u@user.com"


def test_auth_create_teacher(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Send request to create a teacher account for school
    response = client.post(
        "api/auth/register",
        json={
            "name": "Teacher User",
            "username": "teacher_u",
            "password": "123456",
            "email": "teacher_u@user.com",
            "school_id": f"{school.id}",
            "user_type": "teacher",
        },
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    user = SchoolUser.find_by_username("teacher_u")

    assert response.status_code == 200
    assert response.json["message"] == "User created successfully"
    assert user.email == "teacher_u@user.com"


def test_auth_create_owner(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Send request to create a teacher account for school
    response = client.post(
        "api/auth/register",
        json={
            "name": "Owner User",
            "username": "owner_u",
            "password": "123456",
            "email": "owner_u@user.com",
            "school_id": f"{school.id}",
            "user_type": "owner",
        },
        headers={"Authorization": f"Bearer {super_user['token']}"},
    )

    user = SchoolUser.find_by_username("owner_u")

    assert response.status_code == 200
    assert response.json["message"] == "User created successfully"
    assert user.email == "owner_u@user.com"


def test_auth_create_token_super_user(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    response = client.post(
        "api/auth/token", json={"username": "super_u", "password": "123456"}
    )

    assert response.status_code == 200
    assert response.json["token"]
    assert response.json["user"]["name"] == super_user["user"].name
    assert response.json["user"]["role"] == super_user["user"].role
    assert response.json["user"]["public_id"] == super_user["user"].public_id
    assert response.json["user"]["username"] == super_user["user"].username


def test_auth_create_token_teacher(app, client):
    # Reset the database
    db_reset()

    # Create new super user
    super_user = create_super_user(app, client)

    # Send request to create a new school
    school = create_school(client, super_user["token"])

    # Create new owner
    teacher = create_teacher(client, school_id=school.id)

    response = client.post(
        "api/auth/token", json={"username": "teacher_u", "password": "123456"}
    )

    assert response.status_code == 200
    assert response.json["token"]
    assert response.json["user"]["name"] == teacher["user"].name
    assert response.json["user"]["role"] == teacher["user"].role
    assert response.json["user"]["public_id"] == teacher["user"].public_id
    assert response.json["user"]["username"] == teacher["user"].username
