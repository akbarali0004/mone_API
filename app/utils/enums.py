from enum import Enum


class TaskType(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"


class TaskStatus(str, Enum):
    active = "active"
    checking = "checking"
    completed = "completed"
