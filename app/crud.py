from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, date, timedelta
import shutil
import os

from settings import settings
from models import *
from schemas import *

UPLOAD_DIR = settings.UPLOAD_DIR


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
    # created_tasks = []
    for filial_id in task.filials_id:
        db_task = Task(
            description=task.description,
            task_type=task.task_type.value,
            role=task.role,
            filial_id=filial_id,
            task_status="active"
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)


def get_tasks_for_admin(db: Session):
    return db.query(Task).all()
 

def get_tasks_for_user(db: Session, filial_id, role):
    today = date.today()

    is_monday = today.weekday() == 0
    is_first_day = today.day == 1

    filters = [
        Task.task_status == "active",
        Task.filial_id == filial_id,
        Task.role == role
    ]

    task_type_filter = [Task.task_type == "daily"]

    if is_monday:
        task_type_filter.append(Task.task_type == "weekly")

    if is_first_day:
        task_type_filter.append(Task.task_type == "monthly")

    tasks = db.query(Task).filter(
        and_(
            *filters,
            or_(*task_type_filter)
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


    file_path = None
    if not os.path.exists(f"{settings.UPLOAD_DIR}/{date.today()}"):
        os.makedirs(f"{settings.UPLOAD_DIR}/{date.today()}")

    if file:
        extension = file.filename.split(".")[-1]
        new_filename = f"{datetime.now().timestamp()}.{extension}"
        file_path = f"{UPLOAD_DIR}/{date.today()}/{new_filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    task.task_status = "checking"
    db.add(task)
    task_proof = TaskProof(task_id=proof.task_id, text=proof.text, file_path=file_path)
    db.add(task_proof)
    db.commit()
    db.refresh(task_proof)

    return task_proof


from datetime import date, timedelta
from sqlalchemy.orm import Session
from models import Task, TaskProof


def get_task_proof(db: Session):
    one_week_ago = date.today() - timedelta(days=7)

    data = (
        db.query(TaskProof, Task)
        .join(Task, Task.id == TaskProof.task_id)
        .filter(TaskProof.created_date >= one_week_ago)
        .all()
    )

    result = []
    for proof, task in data:
        result.append({
            "id": proof.id,
            "task_id": task.id,
            "description": task.description,
            "task_type": task.task_type,
            "role": task.role,
            "filial_id": task.filial_id,
            "task_status": task.task_status,
            "file_path": proof.file_path,
            "created_date": proof.created_date
        })

    return result



def checker_task_proof_action(current_user, task_id, db, action):
    if current_user.role_rel.name.lower() != "checker":
        raise HTTPException(403, "Role is not checker")
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(404, "Task not found")
    if action == "approve":
        task.task_status = TaskStatus.completed
    elif action == "reject":
        task.task_status = TaskStatus.active
    else:
        raise HTTPException(400, "Invalid action")

    db.commit()

    return {"detail": "Task reviewed successfully"}


# activate
def activate_tasks(db: Session):
    today = datetime.now().date()
    weekday = datetime.today().weekday()

    tasks = db.query(Task).all()

    for task in tasks:
        if task.task_type.value == "daily":
            task.task_status = "active"
        elif task.task_type.value == "weekly" and weekday == 0:
            task.task_status = "active"
        elif task.task_type.value == "monthly" and today.day == 1:
            task.task_status = "active"

    db.commit()