""" Decorators that decode and verify authorization tokens """

from functools import wraps

from flask import request

from FlaskJWT.api.exceptions import ApiUnauthorized
from FlaskJWT.models.refreshToken import RefreshToken
from FlaskJWT.models.user import User


def token_required(f):
    """
    Execute function if request contains valid access token.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        deviceId = request.cookies.get("deviceId")
        setattr(decorated, "deviceId", deviceId)

        tokenPayload = _checkAccessToken()
        for name, val in tokenPayload.items():
            setattr(decorated, name, val)
        return f(*args, **kwargs)

    return decorated


def refresh_token_required(f):
    """
    Execute function if request contains valid refresh token sent from a valid device.
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        deviceId = _checkDeviceId()
        tokenData = _checkRefreshToken(deviceId)
        setattr(decorated, "deviceId", deviceId)
        setattr(decorated, "tokenData", tokenData)
        return f(*args, **kwargs)

    return decorated


def _checkDeviceId():
    """
    Checks that a request contains a cookie with a deviceId
    """

    deviceId = request.cookies.get("deviceId")
    if not deviceId:
        raise ApiUnauthorized(
            description="Unauthorized",
            error="invalid_deviceId",
            errorDescription="deviceId is not valid, please login again",
        )
    return deviceId


def _checkRefreshToken(deviceId):
    """
    Checks refresh token validity given a deviceID
    returns a token object from database
    -----
    parameter:
        deviceId - String
    """

    token = request.cookies.get("refreshToken")

    if not token:
        raise ApiUnauthorized(description="Unauthorized")

    tokenData = RefreshToken.getTokenData(token)

    if not tokenData:
        raise ApiUnauthorized(
            description="token is invalid, please login again",
            error="invalid_token",
            errorDescription="token is invalid, please login again",
        )

    if not tokenData.isValid.success:
        raise ApiUnauthorized(
            description="token expired. Please log in again.",
            error="invalid_token",
            errorDescription="token expired. Please log in again.",
        )

    if tokenData.deviceId != deviceId:
        tokenData.revoke()
        raise ApiUnauthorized(
            description="token is used from unauthorized device, please login again",
            error="invalid_token",
            errorDescription="token is used from unauthorized device, please login again",
        )

    return tokenData


def _checkAccessToken():
    """
    Checks access token validity and returns user data containing publicId
    """

    token = request.headers.get("Authorization")
    if not token:
        raise ApiUnauthorized(description="Unauthorized")
    result = User.decodeAccessToken(token)
    if not result.success:
        raise ApiUnauthorized(
            description=result.error,
            error="invalid_token",
            errorDescription=result.error,
        )
    return result.value
