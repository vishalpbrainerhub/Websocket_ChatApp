from fastapi import FastAPI, Response, status, HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, schemas, utils, oauth2
from fastapi.security import OAuth2PasswordRequestForm



router = APIRouter(tags=["Authentication"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not found")
        if not utils.verify_password(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Password is incorrect")
        
        # create access token
        access_token = oauth2.create_access_token(data = {"user_id":user.id})
        username = user.email
        return {"message": "User logged in successfully", "access_token":access_token,"token_type":"Bearer","username":username}
    except Exception as e:
        print(e)
        return {"message": "Error", "error": e}