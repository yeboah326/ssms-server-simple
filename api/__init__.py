from os import getenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Application instance
app = Flask(__name__)
env_config = getenv("APP_SETTINGS", "api.config.DevelopmentConfig")
app.config.from_object(env_config)

# CORS instance
cors = CORS(app)

# Database instance
db = SQLAlchemy(app, session_options={"expire_on_commit": False})

# Migrate instance
migrate = Migrate(app, db)

# JWT Configurations
jwt = JWTManager(app)

# Import blueprints
from api.auth.controllers import auth
from api.expenditure.controllers import expenditure
from api.school.controllers import school
from api.student.controllers import student
from api.fees.controllers import fees

# Registering the blueprints
app.register_blueprint(auth)
app.register_blueprint(expenditure)
app.register_blueprint(school)
app.register_blueprint(student)
app.register_blueprint(fees)

# Endpoint for handling invalid requests
@app.errorhandler(404)
def page_not_found(error):
    return {"message": "Request does not exist"}
