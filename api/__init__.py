from os import getenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate, migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from dotenv import load_dotenv


load_dotenv()
cors = CORS()
migrate = Migrate()
jwt = JWTManager()

# Initializing database instance
db = SQLAlchemy(session_options={"expire_on_commit": False})


def select_env(env_config: str) -> str:
    """Returns a specific environment confguration

    Args:
        env_config (str): ['prod'. 'dev', 'test']

    Returns:
        config: A string representation of the environment
    """
    env_configs = {"prod": "ProductionConfig", "test": "TestingConfig"}
    return env_configs[env_config]


def add_swagger_config(app: Flask):
    SWAGGER_URL = "/docs"
    API_URL = "/static/swagger.json"
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL, API_URL, config={"app_name": "Work Monitor API"}
    )

    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


def register_blueprints(app):
    from api.auth.controllers import auth
    from api.expenditure.controllers import expenditure
    from api.school.controllers import school
    from api.student.controllers import student
    from api.fees.controllers import fees

    app.register_blueprint(auth)
    app.register_blueprint(expenditure)
    app.register_blueprint(school)
    app.register_blueprint(student)
    app.register_blueprint(fees)

    # Endpoint for handling invalid requests
    @app.errorhandler(404)
    def page_not_found(error):
        return {"message": "Request does not exist"}, 404


def create_app(env_config: str):
    # Create a new application instance
    app = Flask(__name__)
    # Load environment configurations
    ENV_CONFIG = getenv("APP_SETTINGS", f"api.config.{select_env(env_config)}")
    app.config.from_object(ENV_CONFIG)

    register_blueprints(app)

    add_swagger_config(app)

    cors.init_app(app)

    # Database instance
    db.init_app(app)

    # Migrate instance
    migrate.init_app(app, db)

    # JWT Configurations
    jwt.init_app(app)

    return app
