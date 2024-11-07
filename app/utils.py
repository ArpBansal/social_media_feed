from passlib.context import CryptContext
# import secrets

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    # return secrets.compare_digest(plain_password, hashed_password)
    return pwd_context.verify(plain_password, hashed_password)

