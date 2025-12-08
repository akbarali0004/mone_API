from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from datetime import datetime
import shutil
import os

from models import *
from schemas import *


# user
def create_user(db: Session, user: UserCreate):
    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    filial = db.query(Filial).filter(Filial.id == user.filial_id).first()
    if not filial:
        raise HTTPException(status_code=400, detail=f"Filial with id {user.filial_id} not found")
    
    role_rel = db.query(Role).filter(Role.id == user.role).first()
    if not role_rel:
        raise HTTPException(status_code=400, detail=f"Role with id {user.role} not found")

    db_user = User(**user.dict())
    db_user.hash_password(user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return UserResponse(
        user_id=db_user.id,
        full_name=db_user.full_name,
        filial_name=filial.name,
        role=role_rel.name
    )


def get_users(db: Session):
    users = db.query(User).all()
    respons = []
    for user in users:
        respons.append(
            UserResponse(user_id=user.id,
                         full_name=user.full_name,
                         filial_name=user.filial.name,
                         role=user.role_rel.name
                         ))
    return respons

def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User Not Found"}

    db.delete(user)
    db.commit()


# Task
def create_task(db: Session, task: TaskCreate):
    db_task = Task(
        description=task.description,
        task_type=task.task_type.value,
        role=task.role,
        filial_id=task.filial_id,
        task_status="active"
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_tasks_for_admin(db: Session):
    return db.query(Task).all()
 

def get_tasks_for_user(db: Session, filial_id, role):
    tasks = db.query(Task).filter(
        and_(
            Task.task_status == "active",
            Task.filial_id == filial_id,
            Task.role == role
        )
    ).all()
    return tasks

def delete_task(db: Session, task_id: int):
    db.query(Task).filter(Task.id == task_id).delete()
    db.commit()


# Role
def create_role(db: Session, role: RoleCreate):
    db_role = Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session):
    return db.query(Role).all()

def delete_role(db: Session, role_id: int):
    db.query(Role).filter(Role.id == role_id).delete()
    db.commit()


# Task prof
def create_task_proof(db: Session, proof: TaskProofCreate, file):
    task = db.query(Task).filter(Task.id == proof.task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.task_status=="checking":
        raise HTTPException(status_code=409, detail="Task is checking")
    
    if task.task_status=="completed":
        raise HTTPException(status_code=409, detail="Task completed")

    UPLOAD_DIR = "uploads"
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = None

    if file:
        extension = file.filename.split(".")[-1]
        new_filename = f"{datetime.now().timestamp()}.{extension}"
        file_path = f"{UPLOAD_DIR}/{new_filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    task.task_status = "checking"
    db.add(task)
    task_proof = TaskProof(task_id=proof.task_id, text=proof.text, file_path=file_path)
    db.add(task_proof)
    db.commit()
    db.refresh(task_proof)

    return task_proof


# activate
def activate_tasks(db: Session):
    today = datetime.now().date()
    weekday = datetime.today().weekday()  # 0 = Monday

    tasks = db.query(Task).all()

    for task in tasks:
        if task.task_type.value == "daily":
            task.task_status = "active"
        elif task.task_type.value == "weekly" and weekday == 0:  # dushanba
            task.task_status = "active"
        elif task.task_type.value == "monthly" and today.day == 1:  # oy boshida
            task.task_status = "active"

    db.commit()