from os import getenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (JWTManager, create_access_token, get_jwt_identity, jwt_required)

# Application instance
app = Flask(__name__)
env_config = getenv("APP_SETTINGS", "api.config.DevelopmentConfig")
app.config.from_object(env_config)

# CORS instance
cors = CORS(app)

# Database instance
db = SQLAlchemy(app)

# Migrate instance
migrate = Migrate(app,db)

# JWT Configurations
jwt = JWTManager(app)

# Import blueprints
from api.auth.controllers import auth
from api.expenditure.controllers import expenditure

# Registering the blueprints
app.register_blueprint(auth)
app.register_blueprint(expenditure)