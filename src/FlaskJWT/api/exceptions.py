""" Custom HTTPException classes that extend werkzeug.exceptions """

from werkzeug.exceptions import Unauthorized


class ApiUnauthorized(Unauthorized):
    """Raise status code 401 with customizable WWW-Authenticate header."""

    def __init__(self, description="Unauthorized", error=None, errorDescription=None):
        self.description = description
        self.WWWAuthValue = self._getWWWAuthValue(error, errorDescription)
        Unauthorized.__init__(
            self, description=description, response=None, www_authenticate=None
        )

    # Override
    def get_headers(self, environ, scope):
        return [("Content-Type", "text/html"), ("WWW-Authenticate", self.WWWAuthValue)]

    def _getWWWAuthValue(self, error, errorDescription):
        WWWAuthValue = "Bearer"
        if error:
            WWWAuthValue += f', error="{error}"'
        if errorDescription:
            WWWAuthValue += f', error_description="{errorDescription}"'
        return WWWAuthValue
