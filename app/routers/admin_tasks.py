from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from deps import admin_only
from models import *
from schemas import *
from crud import *

router = APIRouter(prefix="/admin", tags=["Admin Tasks"], dependencies=[Depends(admin_only)]) #, dependencies=[Depends(admin_only)]


@router.get("/tasks/", response_model=list[TaskResponse])
def list_tasks(db: Session = Depends(get_db)):
    return get_tasks_for_admin(db)


@router.post("/tasks/") #, response_model=TaskResponse
def create_new_task(task: TaskCreate, db: Session = Depends(get_db)):
    print(task)
    create_task(db, task)
    return {"message":"Success!"}


@router.delete("/tasks/{task_id}", status_code=204)
def remove_task(task_id: int, db: Session = Depends(get_db)):
    delete_task(db, task_id)