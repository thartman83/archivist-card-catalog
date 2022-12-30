import pytest, json, string
from app.appfactory import create_app
from .config import TestConfig

@pytest.fixture(scope='module')
def test_client():
    app = create_app(TestConfig())

    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    yield client

    ctx.pop()

def test_status_nodb(test_client):
    """
    GIVEN a card catalog service
    WHEN the GET /status page is requested
    WHEN the database doesn't exist
    THEN should return 200
    THEN should return that it is not connected to the database
    """
    assert False
