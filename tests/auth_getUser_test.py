"""Unit tests for api.GetUser API endpoint."""

import time
import pytest
from http import HTTPStatus

from flask import url_for
from tests.util import EMAIL, WWW_AUTH_NO_TOKEN, TOKEN_EXPIRED, WWW_AUTH_EXPIRED_TOKEN, registerUser, loginUser, getUser


def test_authUser(client, db):
    registerUser(client)
    response = loginUser(client)
    assert "access_token" in response.json
    accessToken = response.json["access_token"]
    response = getUser(client, accessToken)
    assert response.status_code == HTTPStatus.OK
    assert "email" in response.json and response.json["email"] == EMAIL

def test_authUserNoToken(client, db):
    response = client.get(url_for("api.GetUser"))
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "message" in response.json and response.json["message"] == "Unauthorized"
    assert "WWW-Authenticate" in response.headers
    assert response.headers["WWW-Authenticate"] == WWW_AUTH_NO_TOKEN

@pytest.mark.delay
def test_authUserExpiredToken(client, db):
    registerUser(client)
    response = loginUser(client)
    assert "access_token" in response.json
    access_token = response.json["access_token"]
    time.sleep(6)
    response = getUser(client, access_token)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "message" in response.json and response.json["message"] == TOKEN_EXPIRED
    assert "WWW-Authenticate" in response.headers
    assert response.headers["WWW-Authenticate"] == WWW_AUTH_EXPIRED_TOKEN