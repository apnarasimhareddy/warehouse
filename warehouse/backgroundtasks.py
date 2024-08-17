from typing import Dict, Any
import asyncio
import uuid

task_manager: Dict[str, Dict[str, Any]] = {}
    
async def start_background_task(background_task):
    task_id = str(uuid.uuid4())
    cancel_event = asyncio.Event()
    task = asyncio.create_task(background_task(task_id, cancel_event))
    task_manager[task_id] = {
        "status": "running",
        "result": None,
        "task": task,
        "cancel_event": cancel_event
    }
    return {"task_id": task_id}

async def write_file(id,cancel_event):
    try:
        if cancel_event.is_set():
            task_manager[id]["status"] = "cancelled"
            return
        # while 1==1: # this is testing purpose
            # print(1)
        task_manager[id]["status"] = "completed"
        task_manager[id]["result"] = "Task completed successfully"
    except asyncio.CancelledError:
        task_manager[id]["status"] = "cancelled"
     