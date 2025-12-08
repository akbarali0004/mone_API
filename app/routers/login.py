from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import verify_password, create_access_token
from schemas import UserLogin
from utils.hash_password import *


router = APIRouter(tags=["Login"])


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=400, detail="Username yoki password noto'g'ri")
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Username yoki password noto'g'ri")
    
    token = create_access_token({"user_id": db_user.id})
    
    return {"access_token": token, "token_type": "bearer"}