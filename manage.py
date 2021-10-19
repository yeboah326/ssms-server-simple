from flask.cli import FlaskGroup
from api import db
from api.auth.models import User
cli = FlaskGroup()

@cli.command("create_su")
def create_db():
    user = User(name="Gideon Yeboah Asante", username="kwame",email="kwame@kmail.com",is_super_user=True)
    db.session.add(user)
    db.session.commit()

if __name__== "__main__":
    cli()