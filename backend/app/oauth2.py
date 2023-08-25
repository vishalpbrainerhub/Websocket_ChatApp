from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, models
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

secret_key = settings.secret_key
ALGORITHM = settings.algorithm
access_token_expires_minutes = settings.access_token_expire_minutes

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=access_token_expires_minutes)
    to_encode.update({"exp":expire})
    encoded_jwt = jwt.encode(to_encode,secret_key,algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token : str, credentials_exception):
    try:
           payload =  jwt.decode(token,secret_key,algorithms=[ALGORITHM])
           id: str = payload.get('user_id')
           if id is None:
               raise credentials_exception
           token_data = schemas.TokenData(id=id)     
    except JWTError:
        raise credentials_exception
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate":"Bearer"})

    token = verify_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user