from flask.cli import FlaskGroup
from api import app, db
from api.auth.models import SuperUser

cli = FlaskGroup(app)


@cli.command("create_su")
def create_db():
    """Creates a super user"""
    print("Please enter the following details")
    name = input("Name: ")
    username = input("Username: ")
    password = input("Password: ")
    email = input("Email: ")
    user = SuperUser(name=name, username=username, email=email)
    user.password = password
    db.session.add(user)
    db.session.commit()


if __name__ == "__main__":
    cli()
