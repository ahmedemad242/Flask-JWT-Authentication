"""Unit tests for api.RegisterUser API endpoint """

from http import HTTPStatus
from uuid import uuid4

from FlaskJWT.models.user import User
from tests.util import EMAIL, PASSWORD, FIRSTNAME, LASTNAME, BAD_REQUEST, registerUser

### HTTP Messages
SUCCES_MESSAGE = "successfully registered"
EMAIL_ALREADY_EXISTS = f"{EMAIL} is already registered"


def test_RegisterUser(client, db):
    response = registerUser(client)
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCES_MESSAGE
    assert "token_type" in response.json and response.json["token_type"] == "bearer"
    assert "expires_in" in response.json and response.json["expires_in"] == 5
    assert "access_token" in response.json
    assert "deviceId" in str(response.headers)
    assert "refreshToken" in str(response.headers)
    access_token = response.json["access_token"]
    result = User.decodeAccessToken(access_token)
    assert result.success
    user_dict = result.value
    user = User.findByPublicId(user_dict["publicId"])
    assert user and user.email == EMAIL


def test_RegisterUserWithExistingDeviceId(client, db):
    response = registerUser(client, deviceId=uuid4())
    assert response.status_code == HTTPStatus.CREATED
    assert "status" in response.json and response.json["status"] == "success"
    assert "message" in response.json and response.json["message"] == SUCCES_MESSAGE
    assert "token_type" in response.json and response.json["token_type"] == "bearer"
    assert "expires_in" in response.json and response.json["expires_in"] == 5
    assert "access_token" in response.json
    assert "refreshToken" in str(response.headers)
    access_token = response.json["access_token"]
    result = User.decodeAccessToken(access_token)
    assert result.success
    user_dict = result.value
    user = User.findByPublicId(user_dict["publicId"])
    assert user and user.email == EMAIL


def test_RegisterUserEmailAlreadyExist(client, db):
    User.insert(FIRSTNAME, LASTNAME, EMAIL, PASSWORD)
    response = registerUser(client)
    assert response.status_code == HTTPStatus.CONFLICT
    assert (
        "message" in response.json and response.json["message"] == EMAIL_ALREADY_EXISTS
    )
    assert "token_type" not in response.json
    assert "expires_in" not in response.json
    assert "access_token" not in response.json


def test_RegisterUserInvalidEmail(client, db):
    invalidEmail = "teset12"
    response = registerUser(client, email=invalidEmail)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert "message" in response.json and response.json["message"] == BAD_REQUEST
    assert "token_type" not in response.json
    assert "expires_in" not in response.json
    assert "access_token" not in response.json
    assert "errors" in response.json
    assert "password" not in response.json["errors"]
    assert "email" in response.json["errors"]
    assert response.json["errors"]["email"] == f"{invalidEmail} is not a valid email"
