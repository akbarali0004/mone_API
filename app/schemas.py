from pydantic import BaseModel
from typing import Optional
from utils.enums import TaskStatus, TaskType
from datetime import date


# Roles
class RoleCreate(BaseModel):
    name: str


class RoleResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


# Filials
class FilialCreate(BaseModel):
    name: str


class FilialResponse(BaseModel):
    name: str
    id: int

    model_config = {
        "from_attributes": True
    }


#Users
class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    role: int
    filial_id: Optional[int] = None


class UserCreate(UserBase):
    password: str


class UserResponse(BaseModel):
    user_id: int
    full_name: str
    filial_name: str
    role: str

    model_config = {
        "from_attributes": True
    }


# Tasks
class TaskCreate(BaseModel):
    description: str
    task_type: TaskType
    role: int
    filials_id: list[int]


class TaskResponse(BaseModel):
    id: int
    description: str
    task_type: TaskType
    role: int
    filial_id: int
    task_status: TaskStatus

    model_config = {
        "from_attributes": True
    }


# Task Proof
class TaskProofCreate(BaseModel):
    task_id: int
    text: Optional[str] = None


class TaskProofResponse(BaseModel):
    id: int
    task_id: int
    description: str
    task_type: TaskType
    role: int
    filial_id: int
    task_status: TaskStatus
    file_path: str | None
    created_date: date

    model_config = {
        "from_attributes": True
    }


# Login
class UserLogin(BaseModel):
    username: str
    password: str


# Token
class Token(BaseModel):
    full_name: str
    role: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenRefresh(BaseModel):
    refresh_token: str