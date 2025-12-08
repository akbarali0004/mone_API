from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from deps import admin_only
from models import *
from schemas import *
from crud import *


router = APIRouter(prefix="/admin", tags=["Admin Roles"], dependencies=[Depends(admin_only)])


@router.post("/roles/", response_model=RoleResponse)
def create_new_role(role: RoleCreate, db: Session = Depends(get_db)):
    return create_role(db, role)


@router.get("/roles/", response_model=List[RoleResponse])
def list_roles(db: Session = Depends(get_db)):
    return get_roles(db)


@router.delete("/roles/{role_id}", status_code=204)
def remove_role(role_id: int, db: Session = Depends(get_db)):
    delete_role(db, role_id)
    return {"detail": "Role deleted"}