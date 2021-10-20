from api.auth.models import User


def db_create():
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