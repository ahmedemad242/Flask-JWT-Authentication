""" Unit tests for api.LoginUser API endpoint """

from http import HTTPStatus
from FlaskJWT.models.refreshToken import RefreshToken

from FlaskJWT.models.user import User
from tests.util import EMAIL, registerUser, loginUser

SUCCESS = "successfully logged in"
UNAUTHORIZED = "Email or password are inncorrect."

##TODO:: Rewrite test case with removing the string parsing into a more robust solution


def test_login(client, db):
    registerUser(client)
    response = loginUser(client)
    assert response.status_code == HTTPStatus.OK
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCESS
    assert "access_token" in response.json
    assert "refreshToken" in response.headers["Set-Cookie"]
    access_token = response.json["access_token"]
    result = User.decodeAccessToken(access_token)
    assert result.success
    token_payload = result.value
    user = User.findByPublicId(token_payload["publicId"])
    assert user and user.email == EMAIL


def test_loginWithoutDeviceId(client, db):
    registerUser(client)
    client.cookie_jar.clear()
    response = loginUser(client)
    assert response.status_code == HTTPStatus.OK
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCESS
    assert "access_token" in response.json
    assert "deviceId" in str(response.headers)
    assert "refreshToken" in str(response.headers)
    accessToken = response.json["access_token"]
    result = User.decodeAccessToken(accessToken)
    assert result.success
    token_payload = result.value
    user = User.findByPublicId(token_payload["publicId"])
    assert user and user.email == EMAIL


def test_loginWithExistingValidRefreshToken(client, db):
    registerUser(client)
    response = loginUser(client)
    assert response.status_code == HTTPStatus.OK
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCESS
    refreshToken = response.headers["Set-Cookie"].split(";")[0].split("=")[1]
    response = loginUser(client)
    newRefreshToken = response.headers["Set-Cookie"].split(";")[0].split("=")[1]
    assert not RefreshToken.getTokenData(refreshToken).isValid.success
    assert not newRefreshToken == refreshToken


def test_loginEmailNotExist(client, db):
    response = loginUser(client)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "message" in response.json and response.json["message"] == UNAUTHORIZED
    assert "access_token" not in response.json
