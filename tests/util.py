""" Shared functions and constants for unit testing """

from flask import url_for

### USER
FIRSTNAME = "Ahmed"
LASTNAME = "Emad"
EMAIL = "test@gmail.com"
PASSWORD = "test1234"

### Flask-RESTx messages
BAD_REQUEST = "Input payload validation failed"

### Authuntication messages
WWW_AUTH_NO_TOKEN = "Bearer"
TOKEN_EXPIRED = "token expired. Please log in again."
WWW_AUTH_EXPIRED_TOKEN = (
    f"{WWW_AUTH_NO_TOKEN}, "
    'error="invalid_token", '
    f'error_description="{TOKEN_EXPIRED}"'
)

### Refresh token messages
TOKEN_INVAILD = "token is invalid, please login again"
UNAUTH_DEVICE_ID = "token is used from unauthorized device, please login again"


### Auth
def registerUser(
    test_client,
    firstName=FIRSTNAME,
    lastName=LASTNAME,
    email=EMAIL,
    password=PASSWORD,
    deviceId=None,
):
    return test_client.post(
        url_for("api.RegisterUser"),
        data=f"firstName={firstName}&lastName={lastName}&email={email}&password={password}",
        content_type="application/x-www-form-urlencoded",
    )


def loginUser(test_client, email=EMAIL, password=PASSWORD, deviceId=None):
    return test_client.post(
        url_for("api.LoginUser"),
        data=f"email={email}&password={password}",
        content_type="application/x-www-form-urlencoded",
    )


def getUser(test_client, accessToken):
    return test_client.get(
        url_for("api.GetUser"), headers={"Authorization": f"Bearer {accessToken}"}
    )


def refreshToken(test_client, deviceId, refreshToken):
    test_client.set_cookie("localhost", "deviceId", deviceId)
    test_client.set_cookie("localhost", "refreshToken", refreshToken)
    return test_client.get(url_for("api.Refresh"))


def logoutUser(test_client, accessToken, islogoutAllDevices):
    return test_client.post(
        url_for("api.LogoutUser"),
        headers={"Authorization": f"Bearer {accessToken}"},
        data=f"islogoutAllDevices={islogoutAllDevices}",
        content_type="application/x-www-form-urlencoded",
    )
