""" Unit tests for User model class """

import json
import pytest
import time
from base64 import urlsafe_b64encode, urlsafe_b64decode

from FlaskJWT.models.user import User
from tests.util import TOKEN_EXPIRED



def test_encodeAccessToken(user):
    accesToken = user.encodeAccessToken()
    assert isinstance(accesToken, str)

def test_decodeAccessToken(user):
    accesToken = user.encodeAccessToken()
    result = User.decodeAccessToken(accesToken)
    assert result.success
    user_dict = result.value
    assert user_dict["publicId"] == user.publicId

@pytest.mark.delay
def test_decodeAccessTokenExpired(user):
    accesToken = user.encodeAccessToken()
    time.sleep(6)
    result = User.decodeAccessToken(accesToken)
    assert not result.success
    assert result.error == TOKEN_EXPIRED

def test_decodeAccessTokenInvalid(user):
    accesToken = user.encodeAccessToken()
    split = accesToken.split(".")
    payloadBase64 = split[1]
    padLength = 3 - (len(payloadBase64) % 3)
    payloadBase64 += padLength * "="
    payloadStr = urlsafe_b64decode(payloadBase64)
    payload = json.loads(payloadStr)
    payload["sub"] = "0467124b-3e97-46c4-897d-f4b815d8a511"
    payloadMod = json.dumps(payload)
    payloadModBase64 = urlsafe_b64encode(payloadMod.encode())
    split[1] = payloadModBase64.strip(b"=")
    accessTokenMod = ".".join(str(split))
    assert not accesToken == accessTokenMod
    result = User.decodeAccessToken(accessTokenMod)
    assert not result.success
    assert result.error == "Invalid token. Please log in again."