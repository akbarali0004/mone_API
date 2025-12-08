from fastapi import APIRouter, Depends, UploadFile, File, Form
from sqlalchemy.orm import Session

from database import get_db
from deps import get_current_user
from crud import get_tasks_for_user, create_task_proof
from schemas import TaskResponse, TaskProofCreate
from crud import get_tasks_for_user, create_task_proof
from models import User
from utils.checker_ws import notify_checkers


router = APIRouter(prefix="/worker", tags=["Worker Tasks"])



@router.get("/tasks/", response_model=list[TaskResponse])
def get_task_list(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return get_tasks_for_user(db, current_user.filial_id, current_user.role)


@router.post("/task-proofs/")
async def create_task_proof_(task_id: int = Form(...), text: str | None = Form(None), file: UploadFile | None = File(None), _: User = Depends(get_current_user), db: Session = Depends(get_db)):
    proof = create_task_proof(db, TaskProofCreate(task_id=task_id, text=text), file)

    await notify_checkers(proof)
    return {"message": "Success!"}