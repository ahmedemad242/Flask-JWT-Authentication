""" Refresh token model """

from datetime import datetime
from uuid import uuid4
from sqlalchemy import and_

from FlaskJWT import db
from FlaskJWT.util.result import Result

class RefreshToken(db.Model):
    """
    Refresh token (RT) model is used to whitelist refresh token
    Each RT is linked to a deviceId this is to have different RTs 
    for different devices the user uses.
    --------
    Fields:
        token          -   String      -   uuid4 
        deviceId       -   String      -   uuid4 string represent the device the user is using
        userId         -   int         -   user for whom the token is issued
        createdOn      -   DateTime    -   Date and time the token is issued
        expiresOn      -   DateTime    -   Date and time the token is expired
        revokedOn      -   DateTime    -   Data and time on which the token was revoked - null if not revoked
    """

    __tablename__ = "refreshToken"

    userId = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    deviceId = db.Column(db.String(36), nullable = False)
    token = db.Column(db.String(36), primary_key=True, unique = True, nullable = False, default=lambda: str(uuid4()))
    createdOn = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    expiresOn = db.Column(db.DateTime, nullable=False)
    revokedOn = db.Column(db.DateTime, nullable=True)
    replacedByToken = db.Column(db.String(36), nullable = True)
    

    def __init__(self, userId, expiresOn, deviceId, **kwargs):
        super(RefreshToken, self).__init__(**kwargs)

        self.userId = userId
        self.expiresOn = expiresOn
        self.deviceId = deviceId


    def __repr__(self):
        return f"<Token token={self.token}, revoked={True if self.revokedOn else False}, expiresOn={self.expiresOn}, userId={self.userId}>"

    @classmethod
    def generateRefreshToken(cls, userId, expiresOn, deviceId):
        '''
        inserts a new token to the database and returns the newly created token
        '''
        
        refreshToken = RefreshToken(userId, expiresOn, deviceId)

        db.session.add(refreshToken)
        db.session.commit()

        return refreshToken

    @property
    def isValid(self):
        '''
        Returns Result.success given a token is not expired nor revoked
        '''

        if self.revokedOn is not None:
            return Result.fail('Refresh token has been revoked')
        if not self.isExpired:
            return Result.fail('Refresh token has expired')

        return Result.success('Token is valid')

    @property
    def isExpired(self):
        '''
        Returns true given a token is not expired
        '''

        return datetime.utcnow() < self.expiresOn

    def revoke(self, replacedByToken = None):
        '''
        Revoke a refresh token if it's not expired nor previously revoked
        '''

        if self.isValid.success:
            self.revokedOn = datetime.utcnow()
            if replacedByToken:
                self.replacedByToken = replacedByToken

            db.session.commit()

            return Result.success('The token was revoked successfully')
        else:
            return Result.fail('You cannot revoke an expired token')

    @classmethod
    def getActiveByUserId(cls, userId):
        query = cls.query.filter(and_(cls.userId==userId, datetime.utcnow() < cls.expiresOn, cls.revokedOn == None))
        return query

    @classmethod
    def getActiveByDeviceAndUserId(cls, deviceId, userId):
        query = cls.query.filter(and_(cls.userId==userId, cls.deviceId==deviceId, datetime.utcnow() < cls.expiresOn, cls.revokedOn == None)).first()
        return query

    @classmethod
    def getTokenData(self, token):
        query = self.query.filter_by(token=token).first()
        return query









