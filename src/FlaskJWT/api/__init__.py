""" API blueprint config """

from flask import Blueprint
from flask_restx import Api

from FlaskJWT.api.auth.endpoints import auth_ns

apiBp = Blueprint("api", __name__, url_prefix="/api/v1")
authorizations = {"Bearer": {"type": "apiKey", "in": "header", "name": "Authorization"}}

api = Api(
    apiBp,
    version="1.0",
    title="FlaskJWT APIs",
    description="Welcome to the API documentation site!",
    doc="/ui",
    authorizations=authorizations,
)

api.add_namespace(auth_ns, path="/auth")
