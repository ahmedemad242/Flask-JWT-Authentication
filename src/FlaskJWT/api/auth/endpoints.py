"""API endpoint definitions for /auth namespace."""

from http import HTTPStatus
from flask import request

from flask_restx import Namespace, Resource

from FlaskJWT.api.auth.dto import (
                                registerReqParser, 
                                loginReqParser, 
                                refreshReqParser, 
                                userModel, 
                                logoutParser,
                            )                        
from FlaskJWT.api.auth.business import (
                                    processRegistrationRequest, 
                                    processLoginRequest, 
                                    getLoggedInUser, 
                                    refreshAccessToken, 
                                    processLogoutRequest,
                                )

auth_ns = Namespace(name="auth", validate=True)
auth_ns.models[userModel.name] = userModel

@auth_ns.route("/register", endpoint="RegisterUser")
class RegisterUser(Resource):
    """Handles HTTP requests to URL: /api/v1/auth/register."""

    @auth_ns.expect(registerReqParser)
    @auth_ns.response(int(HTTPStatus.CREATED), "New user was successfully created.")
    @auth_ns.response(int(HTTPStatus.CONFLICT), "Email address is already registered.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Register a new user and return an access token."""
        requestData = registerReqParser.parse_args()
        firstName = requestData.get("firstName")
        lastName = requestData.get("lastName")
        email = requestData.get("email")
        password = requestData.get("password")
        deviceId = requestData.get("deviceId")
        return processRegistrationRequest(firstName, lastName, email, password, deviceId)

@auth_ns.route("/login", endpoint="LoginUser")
class LoginUser(Resource):
    """Handles HTTP requests to URL: /api/v1/auth/login."""

    @auth_ns.expect(loginReqParser)
    @auth_ns.response(int(HTTPStatus.OK), "Login succeeded.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Email or password are inncorrect.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Authenticate an existing user and return an access token."""
        requestData = loginReqParser.parse_args()
        email = requestData.get("email")
        password = requestData.get("password")
        deviceId = requestData.get("deviceId")
        return processLoginRequest(email, password, deviceId)

@auth_ns.route("/user", endpoint="GetUser")
class GetUser(Resource):
    """Handles HTTP requests to URL: /api/v1/auth/user."""

    @auth_ns.doc(security="Bearer")
    @auth_ns.response(int(HTTPStatus.OK), "Token is currently valid.", userModel)
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @auth_ns.marshal_with(userModel)

    def get(self):
        """Validate access token and return user info."""
        return getLoggedInUser()

@auth_ns.route("/refresh", endpoint="Refresh")
class Refresh(Resource):
    """Handles HTTP requests to URL: /api/v1/auth/refresh."""

    @auth_ns.expect(refreshReqParser)
    @auth_ns.doc(security="cookieAuth")
    @auth_ns.response(int(HTTPStatus.OK), "Refresh token successfully refreshed.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token or cookie is invalid or expired.")

    def get(self):
        """Refresh access token given a refresh token and a deviceId"""
        return refreshAccessToken()

@auth_ns.route("/logout", endpoint="LogoutUser")
class LogoutUser(Resource):
    """Handles HTTP requests to URL: /auth/logout."""

    @auth_ns.doc(security="Bearer")
    @auth_ns.expect(logoutParser)
    @auth_ns.response(int(HTTPStatus.OK), "Log out succeeded, token is no longer valid.")
    @auth_ns.response(int(HTTPStatus.BAD_REQUEST), "Validation error.")
    @auth_ns.response(int(HTTPStatus.UNAUTHORIZED), "Token is invalid or expired.")
    @auth_ns.response(int(HTTPStatus.INTERNAL_SERVER_ERROR), "Internal server error.")
    def post(self):
        """Revoke , deauthenticating the current user."""
        requestData = logoutParser.parse_args()
        islogoutAllDevices = requestData.get("email")
        return processLogoutRequest(islogoutAllDevices)