from pydantic import BaseModel
from typing import Optional
from utils.enums import TaskStatus, TaskType


# Roles
class RoleBase(BaseModel):
    name: str


class RoleCreate(RoleBase):
    pass


class RoleResponse(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


# Filials
class FilialBase(BaseModel):
    name: str


class FilialCreate(FilialBase):
    pass


class FilialResponse(FilialBase):
    id: int

    model_config = {
        "from_attributes": True
    }


#Users
class UserBase(BaseModel):
    username: str
    full_name: Optional[str] = None
    role: int
    filial_id: int


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
class TaskBase(BaseModel):
    description: str
    task_type: TaskType
    role: int
    filial_id: int


class TaskCreate(TaskBase):
    pass


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
    text: Optional[str] = None
    file_path: str

    model_config = {
        "from_attributes": True
    }


# Login
class UserLogin(BaseModel):
    username: str
    password: str