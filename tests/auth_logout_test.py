"""Unit tests for api.auth_logout API endpoint."""
import json
from http import HTTPStatus


from FlaskJWT.models.user import User
from FlaskJWT.models.refreshToken import RefreshToken

from tests.util import registerUser, getUser, logoutUser

SUCCESS = "successfully logged out"

##TODO:: Rewrite test case with removing the string parsing into a more robust solution

def test_logoutCurrentDevice(client, db):
    response = registerUser(client)
    deviceId = response.headers["Set-Cookie"].split(";")[0].split("=")[1]
    refreshToken = response.headers[5][1].split(";")[0].split("=")[1]
    accessToken = response.json["access_token"]

    response = getUser(client, accessToken)
    user = json.loads(response.data)
    user = User.findByPublicId(user["publicId"])

    response = logoutUser(client, accessToken, False)
    assert "status" in response.json and response.json["status"] == "success"

    refreshToken = RefreshToken.getActiveByDeviceAndUserId(deviceId, user.id)
    assert not refreshToken 
    
