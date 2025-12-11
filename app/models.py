from sqlalchemy import Column, Integer, String, Text, ForeignKey, Enum, Date
from sqlalchemy.orm import relationship
from database import Base
from datetime import date
from utils.enums import TaskStatus, TaskType

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="role_rel")


class Filial(Base):
    __tablename__ = "filials"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)

    users = relationship("User", back_populates="filial")
    tasks = relationship("Task", back_populates="filial")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=True)
    full_name = Column(String)
    password = Column(String)

    role = Column(Integer, ForeignKey("roles.id"))
    filial_id = Column(Integer, ForeignKey("filials.id"), nullable=True)

    role_rel = relationship("Role", back_populates="users")
    filial = relationship("Filial", back_populates="users")

    def verify_password(self, plain_password):
        return pwd_context.verify(plain_password, self.password)

    def hash_password(self, plain_password):
        self.password = pwd_context.hash(plain_password)


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column(Text)
    task_type = Column(Enum(TaskType, native_enum=False), nullable=False)

    role = Column(Integer, ForeignKey("roles.id"))
    filial_id = Column(Integer, ForeignKey("filials.id"))
    created_date = Column(Date, default=date.today)
    task_status = Column(Enum(TaskStatus, native_enum=False), nullable=False, default="active")

    proofs = relationship("TaskProof", back_populates="task")  
    role_rel = relationship("Role")
    filial = relationship("Filial", back_populates="tasks")


class TaskProof(Base):
    __tablename__ = "task_proofs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))

    text = Column(Text, nullable=True)
    file_path = Column(String, nullable=True)

    created_date = Column(Date, default=date.today)

    # user_id = Column(Integer, ForeignKey("users.id"))

    task = relationship("Task", back_populates="proofs")
