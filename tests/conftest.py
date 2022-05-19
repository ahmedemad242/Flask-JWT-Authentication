""" pytest fixtures """

import pytest

from FlaskJWT import create_app
from FlaskJWT import db as database
from FlaskJWT.models.user import User
from tests.util import EMAIL, PASSWORD, FIRSTNAME, LASTNAME


@pytest.fixture
def app():
    app = create_app("testing")
    return app


@pytest.fixture
def db(app, client, request):
    database.drop_all()
    database.create_all()
    database.session.commit()

    def fin():
        database.session.remove()

    request.addfinalizer(fin)
    return database


@pytest.fixture
def user(db):
    user = User(firstName=FIRSTNAME, lastName=LASTNAME, email=EMAIL, password=PASSWORD)
    db.session.add(user)
    db.session.commit()
    return user
