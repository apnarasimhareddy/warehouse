from fastapi import APIRouter,HTTPException,BackgroundTasks,Request
from warehouse.dependencies import DBSessionDep,sourceDep,queryDep
from warehouse.curd import AsyncDB,SyncTragetDB
from warehouse.backgroundtasks import task_manager,start_background_task,write_file
from warehouse.schemas import TaskStatus,CampaignsSchema,CustomerSchema,WebhookPayload
from warehouse.utilites import Client,APIClient
from pydantic import ValidationError

router = APIRouter()


@router.get('/data/{source}',response_class=list[CampaignsSchema] | list[CustomerSchema])
async def get_data(source,offset,limit,db:DBSessionDep):
    try:
        asyncdb:SyncTragetDB = AsyncDB().targetDB(source,db)
        return await asyncdb.fetch_all(offset,limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/sync/{source}/{endPoint}")
async def sync_data(source:sourceDep,endPoint:str,query:queryDep,db:DBSessionDep):
    try:
        client:APIClient = Client.get_client(source)
        data = await client.get_data(endPoint,query=query)
        asyncdb:SyncTragetDB = AsyncDB().targetDB(source,db)
        await asyncdb.synchronize_data(data)
        return {"status": "success", "message": f"Synchronization from {source} to  completed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/webhook/")
async def handle_webhook(request: Request):
    try:
        payload = await request.json()
        validated_payload = WebhookPayload(**payload)
        return {"status": "success", "received_data": validated_payload.dict()}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=f"Validation error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
    
@router.get("/tasks")
def get_tasks():
    return task_manager

@router.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    task = task_manager.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return TaskStatus(id=task_id, status=task["status"], result=task["result"])

@router.post("/start-task/")
async def start_task(background_tasks: BackgroundTasks):
    try:
        task_id = await start_background_task(write_file)
        return {"task_id": task_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")



@router.post("/task/cancel")
async def cancel_task(task_id: str):
    try:
        task_info = task_manager.get(task_id)
        if not task_info:
            raise HTTPException(status_code=404, detail="Task not found")
        if task_info["status"] in ["completed", "cancelled"]:
            raise HTTPException(status_code=400, detail="Cannot cancel a completed or cancelled task")
        task_info["cancel_event"].set() 
        await task_info["task"] 
        return {"task_id": task_id, "status": task_manager[task_id]["status"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")