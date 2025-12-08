from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
from auth import decode_access_token, SECRET_KEY, ALGORITHM

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_access_token(token)
    if payload in (None, "expired"):
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    user_id = int(payload.get("sub"))
    user = db.query(User).join(User.role_rel).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def admin_only(current_user: User = Depends(get_current_user)):
    if current_user.role_rel.name != "admin":
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return current_user

