from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from deps import admin_checker_only
from models import User
from crud import get_tasks_with_proofs, checker_task_proof_action, get_tasks_for_admin
from schemas import TaskProofResponse, TaskResponse

router = APIRouter(prefix="/checker", tags=["Checker"], dependencies=[Depends(admin_checker_only)])


@router.get("/task-proofs/", response_model=List[TaskProofResponse])
async def websocket_checker(db: Session = Depends(get_db)):
    return get_tasks_with_proofs(db)
    

@router.post("/task-proofs/{task_id}/{action}")
async def review_task(task_id: int, action: str, current_user: User = Depends(admin_checker_only), db: Session = Depends(get_db)):
    return checker_task_proof_action(current_user, task_id, db, action)
