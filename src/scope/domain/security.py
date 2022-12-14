from passlib.context import CryptContext
from passlib.totp import generate_secret as passlib_generate_secret
from jose import JWTError, jwt
from ..config import SECURITY_KEY, ALGORITHM

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_secret_hash(secret):
    return pwd_context.hash(secret)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def generate_secret():
    return passlib_generate_secret()


def generate_client_secret():
    return generate_secret()


def get_hashed_client_secret():
    return get_secret_hash(generate_client_secret())


def decode_jwt(token, algorithm='HS256', verify_signature=False):
    if verify_signature:
        jwt.
        return jwt.decode(token, SECURITY_KEY, algorithms=[algorithm])
    else:
        return jwt.decode(token, key=None, options={"verify_signature": False})
