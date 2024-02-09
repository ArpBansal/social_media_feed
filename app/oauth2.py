from jose import JWTError, jwt
from sqlalchemy.orm import session
from . import schemas, models
from .db import get_db
from datetime import datetime, timedelta
from fastapi import HTTPException, status, Depends
from fastapi.security.oauth2 import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "7a5ed92c90af8bc1b583424261aeaa11f8eb0374e4185bce893f16d9ed214ae5"
ALOGRITHM = "HS256" # TRY AES256
ACCESS_TOKEN_EXPIRE_MINUTES = 300

def create_access_token(data:dict):
    to_encode=data.copy()
    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES) #utcnow() instead of now() ??
    to_encode.update({"exp":expire})

    encode_jwt= jwt.encode(to_encode, SECRET_KEY, algorithm=ALOGRITHM)
    return encode_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALOGRITHM)
        id:str = payload.get("user_id")

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id))
    except JWTError as e:
        print(e)
        raise credentials_exception
    except AssertionError as e:
        print(e)
    return token_data

def get_current_user(db:session=Depends(get_db), token:str=Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED,
    detail=f"could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.Users).filter(models.Users.id==token.id).first()
    # return verify_access_token(token, credentials_exception)
    return user