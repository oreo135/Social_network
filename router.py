from fastapi import APIRouter, Depends
from typing import Annotated
from schemas import STaskAdd, STaskId
from repository import TaskRepository


router = APIRouter(
    prefix='/tasks'
)


@router.post("")
async def add_one(
    task: Annotated[STaskAdd, Depends()]
) -> STaskId:
    task_id = await TaskRepository.add_one(task)
    return {"ok": True, "task_id": task_id}