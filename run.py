import os

from FlaskJWT import create_app, db
from FlaskJWT.models.user import User
from FlaskJWT.models.refreshToken import RefreshToken

app = create_app(os.getenv("FLASK_ENV", "development"))


@app.shell_context_processor
def shell():
    return {"db": db, "User": User, "RefreshToken": RefreshToken}
