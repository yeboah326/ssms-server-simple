import pytest
import os
from api import app as flask_app


@pytest.fixture
def app():
    env_config = os.getenv("APP_SETTINGS", "api.config.DevelopmentConfig")
    flask_app.config.from_object(env_config)
    yield flask_app


@pytest.fixture
def client(app):
    yield app.test_client()