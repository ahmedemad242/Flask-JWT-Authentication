""" Data transfer object for the auth resource """

from flask_restx import Model
from flask_restx.fields import String, DateTime

from flask_restx.inputs import email
from flask_restx.reqparse import RequestParser

###Registeration parser
registerReqParser = RequestParser(bundle_errors=True)

registerReqParser.add_argument(
    name="firstName", type=str, location="form", required=True, nullable=False
)
registerReqParser.add_argument(
    name="lastName", type=str, location="form", required=True, nullable=False
)
registerReqParser.add_argument(
    name="email", type=email(), location="form", required=True, nullable=False
)
#TODO: Add password validation
registerReqParser.add_argument(
    name="password", type=str, location="form", required=True, nullable=False
)
registerReqParser.add_argument(
    name = 'deviceId', type=str, location='cookies', required=False
)

###Login parser
loginReqParser = RequestParser(bundle_errors=True)

loginReqParser.add_argument(
    name="email", type=email(), location="form", required=True, nullable=False
)
loginReqParser.add_argument(
    name="password", type=str, location="form", required=True, nullable=False
)
loginReqParser.add_argument(
    name = 'deviceId', type=str, location='cookies', required=False
)

###Refresh parser
refreshReqParser = RequestParser(bundle_errors=True)

refreshReqParser.add_argument(
    name = 'refreshToken', type=str, location='cookies', required=False
)
refreshReqParser.add_argument(
    name = 'deviceId', type=str, location='cookies', required=False
)

###Logout parser
logoutParser = RequestParser(bundle_errors=True)

logoutParser.add_argument(
    name = 'logoutAllDevices', type=bool, location='form', required=False
)



###User model
userModel = Model(
    "User",
    {
        "email": String,
        "publicId": String,
        "registeredOn": DateTime,
        "tokenExpiresIn": String,
    },
)