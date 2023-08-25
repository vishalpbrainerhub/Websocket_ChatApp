from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, utils,oauth2
from ..database import get_db
# from 



router = APIRouter(
    tags=["Users"]
)


@router.post("/user")
def create_user(request:schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        if db.query(models.User).filter(models.User.email == request.email).first():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"User with email {request.email} already exists")
        
        hashed_password = utils.hash_password(request.password)
        new_user = models.User(email=request.email, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User SignUp in successfully","status":"success"}
    except Exception as e:
        print(e)
        return {"message": "Error", "error": e}


@router.get("/userall")
def get_users(db: Session = Depends(get_db),current_user=Depends(oauth2.get_current_user)):
    try:
        # user except current user
        users = db.query(models.User).filter(models.User.id != current_user.id).all()
        return {"message": "Users retrieved successfully", "data": users}
    except Exception as e:
        print(e)
        return {"message": "Error", "error": e}


