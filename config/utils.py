from datetime import timedelta, datetime
from typing import Union, Dict
from schema.user_schema import User

from jose import jwt
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import  HTTPException

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme:OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_token(user: User) -> Dict:
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.name}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

def handle_exception(func):
    """ Handle exception using decorator """
    def inner(**kwargs):
        try:
            return func(**kwargs)
        except Exception as e:
            raise HTTPException(status_code=423, detail=e)
    
    return inner


@handle_exception
def verify_password(plain_password, hashed_password):
    """ Verify password with plain pwd and hashed pwd """
    return pwd_context.verify(plain_password, hashed_password)


@handle_exception
def get_password_hash(password):
    """ Hash password """
    return pwd_context.hash(password)


@handle_exception
def decode_hash(hashed_password):
    """ decode hashed password """
    return pwd_context.identify(hashed_password)


@handle_exception
def decodeJWT(token: str) -> dict:
    """ Get decoded token """
    decoded_token = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    return decoded_token if decoded_token["exp"] >= int(datetime.utcnow().timestamp()) else None
    

@handle_exception
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None) -> str:
    """ Create JWT token """
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta if expires_delta \
                else datetime.utcnow() + timedelta(minutes=60) 
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f'encoded_jwt {encoded_jwt}')
    return encoded_jwt
  
