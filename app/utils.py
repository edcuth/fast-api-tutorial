from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated='auto') #sets up the hashing algorithm we want to use

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)