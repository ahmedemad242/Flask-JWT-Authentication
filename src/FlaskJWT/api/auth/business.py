""" logic for /auth API endpoints."""

from http import HTTPStatus
from datetime import datetime, timedelta
from uuid import uuid4

from flask import current_app, jsonify, make_response
from flask_restx import abort

from FlaskJWT.models.user import User
from FlaskJWT.models.refreshToken import RefreshToken
from FlaskJWT.api.auth.decorators import token_required, refresh_token_required


def processRegistrationRequest(firstName, lastName, email, password, deviceId=None):
    """
    Process requests to endpoint /auth/register
    return HTTP response containing access token, refresh token, and deviceID
    -------
    parameters:
        firstName   - String    -
        lastName    - String    -
        email       - String    -
        password    - String    -
        deviceId    - String    - Sent if the device has a cookie set with deviceId value
    """

    if User.findByEmail(email):
        abort(HTTPStatus.CONFLICT, f"{email} is already registered", status="fail")
    user = User.insert(firstName, lastName, email, password)

    accessToken = user.encodeAccessToken()
    response = make_response(
        _successfulAuthResponse(
            accessToken, HTTPStatus.CREATED, "successfully registered"
        )
    )

    if not deviceId:
        deviceId = _setDeviceIdCookie(response)

    refreshExpireTime = datetime.utcnow() + timedelta(
        seconds=_getRefreshTokenExpireTime()
    )
    refreshToken = RefreshToken.generateRefreshToken(
        user.id, refreshExpireTime, deviceId
    )

    _setRefreshTokenCookie(response, refreshToken.token)

    return response


def processLoginRequest(email, password, deviceId):
    """
    Process requests to endpoint /auth/login
    return HTTP response containing access token, refresh token, and deviceID
    -------
    parameters:
        email       - String    -
        password    - String    -
        deviceId    - String    - Sent if the device has a cookie set with deviceId value
    """

    user = User.findByEmail(email)
    if not user or not user.checkPassword(password):
        abort(
            HTTPStatus.UNAUTHORIZED, "Email or password are inncorrect.", status="fail"
        )

    accessToken = user.encodeAccessToken()
    response = make_response(
        _successfulAuthResponse(accessToken, HTTPStatus.OK, "successfully logged in")
    )

    if not deviceId:
        deviceId = _setDeviceIdCookie(response)

    currentValid = RefreshToken.getActiveByDeviceAndUserId(deviceId, user.id)

    refreshExpireTime = datetime.utcnow() + timedelta(
        seconds=_getRefreshTokenExpireTime()
    )
    refreshToken = RefreshToken.generateRefreshToken(
        user.id, refreshExpireTime, deviceId
    )
    if currentValid:
        currentValid.revoke(refreshToken.token)

    _setRefreshTokenCookie(response, refreshToken.token)

    return response


@token_required
def processLogoutRequest(islogoutAllDevices):
    userPublicId = processLogoutRequest.publicId
    user = User.findByPublicId(userPublicId)
    deviceId = processLogoutRequest.deviceId

    if islogoutAllDevices:
        tokens = RefreshToken.getActiveByUserId(user.id)
        if len(tokens) > 0:
            for tokenData in tokens:
                tokenData.revoke()
    else:
        tokenData = RefreshToken.getActiveByDeviceAndUserId(deviceId, user.id)
        if tokenData:
            tokenData.revoke()

    return dict(status="success", message="successfully logged out"), HTTPStatus.OK


@token_required
def getLoggedInUser():
    """
    Process requests to endpoint /auth/GetUser
    return HTTP response containing user
    """

    publicId = getLoggedInUser.publicId
    expiresAt = getLoggedInUser.exp

    user = User.findByPublicId(publicId)
    user.tokenExpiresIn = expiresAt
    return user


@refresh_token_required
def refreshAccessToken():
    """
    Process requests to endpoint /auth/refresh
    return HTTP response containing refresh token
    """

    tokenData = refreshAccessToken.tokenData
    accessToken = tokenData.user.encodeAccessToken()

    response = make_response(
        _successfulAuthResponse(
            accessToken, HTTPStatus.OK, "successfully refreshed access token"
        )
    )

    refreshExpireTime = datetime.utcnow() + timedelta(
        seconds=_getRefreshTokenExpireTime()
    )
    refreshToken = RefreshToken.generateRefreshToken(
        tokenData.userId, refreshExpireTime, refreshAccessToken.deviceId
    )

    tokenData.revoke(refreshToken.token)

    _setRefreshTokenCookie(response, refreshToken.token)

    return response


def _setDeviceIdCookie(response):
    """
    Sets a cookie with the deviceId on a given response and returns the id
    -----
    parameters:
        response - Flask response object
    """

    deviceId = _generateDeviceId()
    response.set_cookie(
        "deviceId", deviceId, max_age=2147483647, httponly=True, samesite="Strict"
    )

    return deviceId


def _generateDeviceId():
    """
    returns a uuid4 string
    """

    return str(uuid4())


def _setRefreshTokenCookie(response, refreshToken):
    """
    Sets a cookie with the refreshToken on a given response and refreshToken
    -----
    parameters:
        response        - Flask response object
        refreshToken    - String
    """

    response.set_cookie(
        "refreshToken",
        refreshToken,
        max_age=_getRefreshTokenExpireTime(),
        httponly=True,
        samesite="Strict",
        path="/api/v1/auth/refresh",
    )


def _successfulAuthResponse(accessToken, status_code, message):
    """
    returns a response body for a successful authenticatoin request
    -----
    parameters:
        accessToken     - String        -
        status_code     - HTTPStatus    - HTTP status to be sent with response
        message         - String        - Message in response body
    """

    response = jsonify(
        status="success",
        message=message,
        access_token=accessToken,
        token_type="bearer",
        expires_in=_getAccessTokenExpireTime(),
    )
    response.status_code = status_code
    response.headers["Cache-Control"] = "no-store"
    response.headers["Pragma"] = "no-cache"

    return response


def _getAccessTokenExpireTime():
    """
    returns the access token expiration time from enviromntal variables
    """

    tokenAgeHours = current_app.config.get("TOKEN_EXPIRE_HOURS")
    tokenAgeMinutes = current_app.config.get("TOKEN_EXPIRE_MINUTES")
    expireTimeSeconds = tokenAgeHours * 3600 + tokenAgeMinutes * 60
    return expireTimeSeconds if not current_app.config["TESTING"] else 5


def _getRefreshTokenExpireTime():
    """
    returns the refresh token expiration time from enviromntal variables
    """

    tokenAgeHours = current_app.config.get("REFRESH_TOKEN_EXPIRE_HOURS")
    tokenAgeMinutes = current_app.config.get("REFRESH_TOKEN_EXPIRE_MINUTES")
    expireTimeSeconds = tokenAgeHours * 3600 + tokenAgeMinutes * 60
    return expireTimeSeconds if not current_app.config["TESTING"] else 6
