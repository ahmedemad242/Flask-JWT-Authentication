""" User model """

from datetime import datetime, timedelta
from uuid import uuid4

import jwt
from flask import current_app

from FlaskJWT import db, bcrypt
from FlaskJWT.util.result import Result


class User(db.Model):
    """
    User model to store the login creadentials
    Create a table named client in the database
    --------
    Fields:
        id             -   int         -   id of user in database
        publicId       -   string      -   Public Id of user, stored in tokens
        firstName      -   String      -   first name of user
        lastName       -   String      -   last name of user
        email          -   String      -   Email of user used for login
        passwordHash   -   String      -   Hash of user's password
        registeredOn   -   datetime    -   Date & time of account creation
        lastLogin      -   datetime    -   last time the user sent a request to the server
        tokens         -   List        -   List of all refresh tokens used by the user
    """

    __tablename__ = "client"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publicId = db.Column(db.String(36), unique=True, default=lambda: str(uuid4()))
    firstName = db.Column(db.String(20), nullable=False)
    lastName = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    passwordHash = db.Column(db.String(100), nullable=False)
    registeredOn = db.Column(db.DateTime, default=datetime.utcnow)
    lastLogin = db.Column(db.DateTime, default=datetime.utcnow)
    tokens = db.relationship("RefreshToken", backref="user", lazy=True)

    def __init__(self, firstName, lastName, email, password, **kwargs):
        super(User, self).__init__(**kwargs)

        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password

    def __repr__(self):
        return f"<User email={self.email}, public_id={self.publicId}>"

    @classmethod
    def insert(cls, firstName, lastName, email, password):
        """
        inserts user to the database and returns the newly created user
        """

        user = User(firstName, lastName, email, password)
        db.session.add(user)
        db.session.commit()

        return user

    @classmethod
    def delete(cls, id):
        """
        removes user from the database
        """

        user = cls.query.findByID(id)
        db.session.delete(user)
        db.session.commit()

    @classmethod
    def update(cls, id, firstName, lastName, email, password):
        """
        updates existing user record and returns the updated user
        """

        user = cls.query.get(id)

        user.firstName = firstName
        user.lastName = lastName
        user.email = email
        user.password = password

        db.session.commit()

        return user

    @classmethod
    def findByEmail(cls, email):
        """
        Returns user data given a valid email
        -----
        parameters:
            email - String
        """

        user = cls.query.filter_by(email=email).first()
        return user

    @classmethod
    def findByPublicId(cls, publicId):
        """
        Returns user data given a valid publicId
        -----
        parameters:
            publicId - String
        """

        user = cls.query.filter_by(publicId=publicId).first()
        return user

    @classmethod
    def findByID(cls, id):
        """
        Returns user data given a valid id
        -----
        parameters:
            id - int
        """

        user = cls.query.filter_by(id=id).first()
        return user

    @property
    def password(self):
        raise AttributeError("password: write-only field")

    @password.setter
    def password(self, password):
        """
        Sets password in database as a hash
        -----
        parameters:
            password - String
        """

        log_rounds = current_app.config.get("BCRYPT_LOG_ROUNDS")
        hash_bytes = bcrypt.generate_password_hash(password, log_rounds)
        self.passwordHash = hash_bytes.decode("utf-8")

    def checkPassword(self, password):
        """
        Returns true if a given password matches database
        -----
        parameters:
            password - String
        """

        return bcrypt.check_password_hash(self.passwordHash, password)

    def encodeAccessToken(self):
        """
        Returns an access token for a user
        """

        timeNow = datetime.utcnow()
        tokenAgeHours = current_app.config.get("TOKEN_EXPIRE_HOURS")
        tokenAgeMin = current_app.config.get("TOKEN_EXPIRE_MINUTES")
        expire = timeNow + timedelta(hours=tokenAgeHours, minutes=tokenAgeMin)
        if current_app.config["TESTING"]:
            expire = timeNow + timedelta(seconds=5)
        payload = {
            "exp": expire,
            "iat": timeNow,
            "sub": self.publicId,
        }
        key = current_app.config.get("SECRET_KEY")
        return jwt.encode(payload, key, algorithm="HS256")

    @staticmethod
    def decodeAccessToken(accessToken):
        """
        Returns user given a non expired valid access token
         parameters:
            accessToken - String
        """

        if isinstance(accessToken, bytes):
            accessToken = accessToken.decode("ascii")
        if accessToken.startswith("Bearer "):
            split = accessToken.split("Bearer")
            accessToken = split[1].strip()
        try:
            key = current_app.config.get("SECRET_KEY")
            payload = jwt.decode(accessToken, key, algorithms=["HS256"])
        # TODO: handle these errors
        except jwt.ExpiredSignatureError:
            return Result.fail("token expired. Please log in again.")
        except jwt.InvalidTokenError:
            return Result.fail("Invalid token. Please log in again.")

        user_dict = {
            "publicId": payload["sub"],
            "token": accessToken,
            "exp": payload["exp"],
        }

        return Result.success(user_dict)
