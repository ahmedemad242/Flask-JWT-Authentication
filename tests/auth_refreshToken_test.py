"""Unit tests for api.Refresh API endpoint """

import time
import json
from uuid import uuid4
import pytest
from http import HTTPStatus


from FlaskJWT.models.user import User
from FlaskJWT.models.refreshToken import RefreshToken
from tests.util import EMAIL, registerUser, loginUser, refreshToken as refreshTokenHelper, getUser,\
     EMAIL, TOKEN_EXPIRED, TOKEN_INVAILD, UNAUTH_DEVICE_ID

##TODO:: Rewrite test case with removing the string parsing into a more robust solution

@pytest.mark.delay
def test_refreshToken(client, db):
    response = registerUser(client)
    deviceId = response.headers["Set-Cookie"].split(";")[0].split("=")[1]
    refreshToken = response.headers[5][1].split(";")[0].split("=")[1]
    accessToken = response.json["access_token"]

    response = getUser(client, accessToken)
    user = json.loads(response.data)

    assert user['email'] == EMAIL

    time.sleep(1)

    response = refreshTokenHelper(client, deviceId, refreshToken)

    newRefreshToken = response.headers["Set-Cookie"].split(";")[0].split("=")[1]
    newAccessToken = response.json["access_token"]
    
    assert newRefreshToken != refreshToken
    assert not RefreshToken.getTokenData(refreshToken).isValid.success
    assert newAccessToken != accessToken

@pytest.mark.delay
def test_expiredRefreshToken(client, db):
    response = registerUser(client)
    deviceId = response.headers["Set-Cookie"].split(";")[0].split("=")[1]
    refreshToken = response.headers[5][1].split(";")[0].split("=")[1]

    time.sleep(7)

    response = refreshTokenHelper(client, deviceId, refreshToken)

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "message" in response.json 
    assert response.json["message"] == TOKEN_EXPIRED
    assert "WWW-Authenticate" in response.headers

def test_invaildRefreshToken(client, db):
    response = registerUser(client)
    deviceId = response.headers["Set-Cookie"].split(";")[0].split("=")[1]

    response = refreshTokenHelper(client, deviceId, str(uuid4()))

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "message" in response.json 
    assert response.json["message"] == TOKEN_INVAILD
    assert "WWW-Authenticate" in response.headers

def test_unauthDevice(client, db):
    response = registerUser(client)
    refreshToken = response.headers[5][1].split(";")[0].split("=")[1]

    response = refreshTokenHelper(client, str(uuid4()), refreshToken)

    assert not RefreshToken.getTokenData(refreshToken).isValid.success

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert "message" in response.json 
    assert response.json["message"] == UNAUTH_DEVICE_ID
    assert "WWW-Authenticate" in response.headers



