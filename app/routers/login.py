from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import create_access_token, create_refresh_token, verify_token
from schemas import UserLogin, Token, TokenRefresh
from utils.hash_password import *


router = APIRouter(tags=["Login"])


@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Username yoki password noto'g'ri")
    
    payload = {
        "user_id": db_user.id,
        "role": db_user.role_rel.name,
        "filial_id": db_user.filial_id
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token(payload)

    return {"full_name":db_user.full_name, "role":db_user.role_rel.name, "access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}


@router.post("/refresh", response_model=Token)
def refresh_token(token_data: TokenRefresh):
    try:
        payload = verify_token(token_data.refresh_token)
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

    new_access = create_access_token(payload)
    new_refresh = create_refresh_token(payload)

    return {"access_token": new_access, "refresh_token": new_refresh, "token_type": "bearer"}