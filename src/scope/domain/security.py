from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_secret_hash(secret):
    return pwd_context.hash(secret)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
