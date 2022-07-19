import os

from dotenv import load_dotenv

load_dotenv(".env")

from FlaskJWT import create_app, db
from FlaskJWT.models.user import User
from FlaskJWT.models.refreshToken import RefreshToken

app = create_app(os.getenv("FLASK_ENV", "production"))


@app.shell_context_processor
def shell():
    return {"db": db, "User": User, "RefreshToken": RefreshToken}


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
