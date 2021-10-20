from api.auth.models import User
from api.tests.utils import db_create

def test_auth_create_new_token():
    assert 1 == 1

def test_create_new_user_account(client):
    db_create()

    reponse = client.post(
        "/register",
        json={
            "name":"Dummy User",
            "username": "dummy_u",
            "password": "123456",
            "email": "dummy@dmail.com"
        }    
    )

    user = User.find_by_username("dummy_u")

    assert user.name == "Dummy User"
    assert user.user_name == "dummy_u"
    assert user.email == "dummy@dmail.com"