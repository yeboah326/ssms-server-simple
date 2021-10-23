from api.auth.models import User, SuperUser
from api.school.models import School

def db_reset():
    """db_reset() - Drops all the data in all tables before the test runs
    """
    School.query.delete()
    SuperUser.query.delete()
    User.query.delete()

def create_new_user(app, client):
    client.post(
        "/register",
        json={
            "name":"Dummy User",
            "username": "dummy_u",
            "password": "123456",
            "email": "dummy@dmail.com"
        }
    )

    user = User.find_by_username("dummy_u")

    return user

def create_school(app, client):
    """Creates an instance of school
    """
    db_reset()

    client.post(
        "api/school/create",
        json={
            "name": "Rachael Shilo School Complex",
            "location": "Accra"
        }
    )

    school = School.find_by_name("Rachael Shilo School Complex")

    return school