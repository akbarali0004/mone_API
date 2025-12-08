from fastapi import APIRouter, WebSocket, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from database import get_db
from deps import get_current_user
from models import User, Task
from utils.enums import TaskStatus
from utils.checker_ws import connected_checkers


router = APIRouter(prefix="/ws/", tags=["Checker"])

@router.websocket("/checker/")
async def websocket_checker(ws: WebSocket, current_user: User = Depends(get_current_user)):
    if current_user.role != "checker":
        await ws.close(code=1008)
        return
    await ws.accept()
    connected_checkers.append(ws)
    # try:
    #     while True:
    #         await ws.receive_text()
    # except WebSocketDisconnect:
    #     connected_checkers.remove(ws)


@router.post("/task-proofs/{task_id}/approve")
def approve_task(task_id: int, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if User.role!="checker":
        raise HTTPException(403, "Role is not checker")
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.task_status = "completed"
    db.commit()
    return {"message": "Task approved!"}


@router.post("/task-proofs/{task_id}/review")
def review_task(task_id: int, action: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if action == "approve":
        task.task_status = TaskStatus.completed
    elif action == "reject":
        task.task_status = TaskStatus.active
    else:
        raise HTTPException(status_code=400, detail="Invalid action")

    db.commit()

    return {"message": f"Task {task.task_status}!"}


router.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")