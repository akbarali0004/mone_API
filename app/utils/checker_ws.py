from fastapi import WebSocket
import json

connected_checkers: list[WebSocket] = []


async def notify_checkers(proof):
    message = {
        "task_id": proof.task_id,
        "text": proof.text,
        "file_url": f"/uploads/{proof.file_path}" if proof.file_path else None
    }
    
    for ws in connected_checkers:
        try:
            await ws.send_text(json.dumps(message))
        except:
            connected_checkers.remove(ws)
