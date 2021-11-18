from dotenv import load_dotenv
from api import create_app
import os
from api.tests.utils_test import (
    create_owner,
    create_super_user,
    create_school,
    create_academic_year,
    create_class,
    create_multiple_students,
    db_reset,
)

load_dotenv()


def test_app_config(app):
    assert app.config["TESTING"] == True
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_TEST_URL")


def test_app_testing_config():
    app = create_app("test")
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_TEST_URL")


def test_app_developoment_config():
    app = create_app("prod")
    assert app.config["SQLALCHEMY_DATABASE_URI"] == os.getenv("DATABASE_URL")


def test_404(app, client):
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
    school_class = create_class(client, super_user, academic_year, 800)

    # Create multiple students student
    create_multiple_students(client, super_user, school_class)

    response = client.get(
        f"api/student/class/{school_class.id}/",
        headers={"Authorization": f"Bearer {owner['token']}"},
    )
    print(response.json)
    assert response.status_code == 404
    assert response.json["message"] == "Request does not exist"
