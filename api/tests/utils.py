from api import db
from api.auth.models import SchoolUser, User, SuperUser
from api.school.models import School

def db_reset():
    """db_reset() - Drops all the data in all tables before the test runs
    """
    SuperUser.query.delete()
    SchoolUser.query.delete()
    School.query.delete()
    User.query.delete()
    db.session.commit()


def create_school(app, client, super_user_token):
    """Creates an instance of school
    """
        
    client.post(
        "api/school/create",
        json={
            "name": "Rachael Shilo School Complex",
            "location": "Accra"
        },
        headers={"Authorization": f"Bearer {super_user_token}"},
    )

    school = School.find_by_name("Rachael Shilo School Complex")

    return {"school": school}

def create_new_super_user(app, client):
    # Create and store user
    client.post(
        "/api/auth/register",
        json={
            "name":"Super User",
            "username": "super_u",
            "password": "123456",
            "email": "super_u@user.com",
            "user_type": "super_user"
        }    
    )

    super_user = SuperUser.find_by_email("super_u@user.com")

    # Login user to generate the token
    response = client.post(
        "api/auth/token",
        json={
            "username": "super_u",
            "password": "123456"
        }
    )

    return { "user": super_user, "token": response.json["token"] }

def create_new_admin(app, client):
    # Send request to create a new school
    school = create_school()

    # Create and store user
    client.post(
        "/register",
        json={
            "name":"Admin User",
            "username": "admin_u",
            "password": "123456",
            "email": "admin_u@user.com",
            "school_id": f"{school.id}",
            "user_type": "admin"
        }    
    )

    admin = SchoolUser.find_by_email("admin_u@user.com")

    # Login user to generate the token
    response = client.post(
        "api/auth/token",
        json={
            "username": "admin_u",
            "password": "123456"
        }
    )

    return {"user" : admin, "token": response.json["token"]}

def create_new_auditor(app,client):
    # Send request to create a new school
    school = create_school()

    # Create the user to be stored
    reponse = client.post(
        "/register",
        json={
            "name":"Auditor User",
            "username": "auditor_u",
            "password": "123456",
            "email": "auditor_u@user.com",
            "school_id": f"{school.id}",
            "user_type": "auditor"
        }    
    )

    auditor = SchoolUser.find_by_email("auditor_u@user.com")

    # Login user to generate the token
    response = client.post(
        "api/auth/token",
        json={
            "username": "auditor_u",
            "password": "123456"
        }
    )

    return {"user": auditor, "token": response.json["token"]}

# TODO: Create new teacher
def create_new_teacher(app,client):
    # Send request to create a new school
    school = create_school()

    # Send request to create a teacher account for school
    client.post(
        "/register",
        json={
            "name":"Teacher User",
            "username": "teacher_u",
            "password": "123456",
            "email": "teacher_u@user.com",
            "school_id": f"{school.id}",
            "user_type": "teacher"
        }    
    )

    teacher = SchoolUser.find_by_email("teacher_u@user.com")

    # Login user to generate the token
    response = client.post(
        "api/auth/token",
        json={
            "username": "teacher_u",
            "password": "123456"
        }
    )


    return {"user":teacher, "token":response.json["token"]}