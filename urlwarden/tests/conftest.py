import pytest

from urlwarden.app import create_app


@pytest.fixture(scope="session")
def app():
    """
    Setup our Flask test app (this only gets executed once)

    :return: Flask app
    """
    params = {
        "DEBUG": False,
        "TESTING": True,
    }

    _app = create_app(settings_override=params)

    # Establish an application context before running the tests.
    ctx = _app.app_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="function")
def client(app):
    """
    Setup our app client (this gets executed once for each test function)

    :param app: Pytest fixture
    :return: Flask app client
    """
    yield app.test_client()
