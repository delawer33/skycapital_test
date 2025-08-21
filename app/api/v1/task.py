import logging
import uuid
from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from typing import List

from app.config.settings import get_settings
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate, TaskDelete
from app.models.task import Task, TaskStatus
from app.dependencies import get_async_db_session

app_settings = get_settings()

router = APIRouter(prefix="/tasks", tags=["Task"])

logger = logging.getLogger("app.task")
if app_settings.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)


@router.post("/", response_model=TaskResponse)
async def create_task(
    task_data: TaskCreate, db: AsyncSession = Depends(get_async_db_session)
):
    logger.info(f"Создание задачи с title: {task_data.title}")

    task = Task(**task_data.model_dump())

    try:
        db.add(task)
        await db.flush()
        await db.refresh(task)
        await db.commit()
        logger.info(f"Создана задача с UUID: {task.uuid}")

        return task

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при создании задачи: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка базы данных",
        )

    except Exception as e:
        logger.error(f"Ошибка при создании задачи: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неизввестная ошибка",
        )


@router.get("/{task_uuid}", response_model=TaskResponse)
async def get_task(
    task_uuid: uuid.UUID, db: AsyncSession = Depends(get_async_db_session)
):
    result = await db.execute(select(Task).where(Task.uuid == task_uuid))
    task = result.scalar_one_or_none()
    if not task:
        logger.error(f"Ошибка при получении задачи")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с uuid={task_uuid} не найдена",
        )
    return task


@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    db: AsyncSession = Depends(get_async_db_session),
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
):
    try:
        query = select(Task).offset(offset).limit(limit)
        result = await db.execute(query)
        tasks = result.scalars().all()
        return tasks

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при получении списка задач: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении задачи",
        )

    except Exception as e:
        logger.error(f"Ошибка при получении списка задач: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неизввестная ошибка",
        )


@router.patch("/{task_uuid}", response_model=TaskResponse)
async def update_task(
    task_uuid: uuid.UUID,
    task_data: TaskUpdate,
    db: AsyncSession = Depends(get_async_db_session),
):
    result = await db.execute(select(Task).where(Task.uuid == task_uuid))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с uuid={task_uuid} не найдена",
        )

    update_data = task_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(task, key, value)

    try:
        db.add(task)
        await db.commit()
        await db.refresh(task)
        return task

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при изменении задачи: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при обновлении задачи",
        )

    except Exception as e:
        logger.error(f"Ошибка при изменении задачи: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неизввестная ошибка",
        )


@router.delete("/{task_uuid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_uuid: uuid.UUID, db: AsyncSession = Depends(get_async_db_session)
):
    result = await db.execute(select(Task).where(Task.uuid == task_uuid))
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Задача с uuid={task_uuid} не найдена",
        )

    try:
        await db.delete(task)
        await db.commit()

    except SQLAlchemyError as e:
        logger.error(f"Ошибка при удалении задачи: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ошибка при удалении задачи",
        )

    except Exception as e:
        logger.error(f"Ошибка при удалении задачи: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Неизввестная ошибка",
        )
