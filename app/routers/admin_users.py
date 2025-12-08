from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import UserCreate, UserResponse
from deps import admin_only
from crud import get_users, create_user, delete_user

router = APIRouter(prefix="/admin", tags=["Admin Users"], dependencies=[Depends(admin_only)])


@router.get("/users/", response_model=list[UserResponse])
def list_users(db: Session = Depends(get_db)):
    return get_users(db)


@router.post("/create", response_model=UserResponse)
def create_user_(user: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user)


@router.delete("/{user_id}")
def delete_user_(user_id: int, db: Session = Depends(get_db)):
    return delete_user(db, user_id)
