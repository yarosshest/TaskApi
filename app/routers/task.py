from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Annotated
from pydantic import BaseModel
from db.models import Task, User  # Обязательно укажите правильный путь к вашей модели Task
from db.interfaces.DatabaseInterface import \
    DatabaseInterface  # Убедитесь, что импортируете правильный интерфейс базы данных
from db.database import get_db_session  # Импортируйте свою зависимость для получения сессии базы данных
from models.models import TaskCreate, TaskUpdate, Task as pdTask
from security.security import get_current_user


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"],
)
@router.post("/", response_model=pdTask)
async def create_task(task: TaskCreate,
                      user: Annotated[User, Depends(get_current_user)],
                      db: Annotated[AsyncSession, Depends(get_db_session)]):
    db_interface = DatabaseInterface(db)
    new_task = Task(**task.dict())
    return await db_interface.add(new_task)


@router.get("/", response_model=List[pdTask])
async def read_tasks(user: Annotated[User, Depends(get_current_user)],
                     skip: int = 0,
                     limit: int = 10,
                     db: AsyncSession = Depends(get_db_session)):
    db_interface = DatabaseInterface(db)
    tasks = await db_interface.get_all(Task)
    return tasks[skip: skip + limit]


@router.get("/{task_id}", response_model=pdTask)
async def read_task(task_id: int,
                    user: Annotated[User, Depends(get_current_user)],
                    db: AsyncSession = Depends(get_db_session)):
    db_interface = DatabaseInterface(db)
    task = await db_interface.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/{task_id}", response_model=pdTask)
async def update_task(task_id: int,
                      user: Annotated[User, Depends(get_current_user)],
                      task_update: TaskUpdate, db: AsyncSession = Depends(get_db_session)):
    db_interface = DatabaseInterface(db)
    task = await db_interface.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    # Обновляем только те поля, которые были переданы
    updated_task = await db_interface.update(task, **task_update.dict(exclude_unset=True))
    return updated_task


@router.delete("/{task_id}", response_model=dict)
async def delete_task(task_id: int,
                      user: Annotated[User, Depends(get_current_user)],
                      db: AsyncSession = Depends(get_db_session)):
    db_interface = DatabaseInterface(db)
    task = await db_interface.get(Task, task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    await db_interface.delete(task)
    return {"detail": "Task deleted successfully"}
