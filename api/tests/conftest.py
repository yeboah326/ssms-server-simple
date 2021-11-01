import pytest
from api import create_app, db as _db


@pytest.fixture
def app():
    flask_app = create_app("test")
    flask_app.app_context().push()
    yield flask_app


@pytest.fixture
def client(app):
    yield app.test_client()
