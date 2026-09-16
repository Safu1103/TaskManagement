from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal


api = FastAPI(title="Task Management API")


class Task(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    status: Literal["pending", "in_progress", "completed"]
    priority: Literal["low", "medium", "high"]


tasks = [
    Task(
        id=1,
        title="Study FastAPI",
        description="Learn FastAPI basics",
        status="pending",
        priority="high"
    ),
    Task(
        id=2,
        title="Write Assignment",
        description="Complete the API assignment",
        status="in_progress",
        priority="medium"
    )
]


# GET - Get all tasks
@api.get("/tasks")
def get_tasks():
    return tasks


# GET - Get one task
@api.get("/tasks/{task_id}")
def get_task(task_id: int):
    for task in tasks:
        if task.id == task_id:
            return task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# POST - Create a new task
@api.post("/tasks", status_code=201)
def create_task(task: Task):
    for existing_task in tasks:
        if existing_task.id == task.id:
            raise HTTPException(
                status_code=400,
                detail="Task ID already exists"
            )

    tasks.append(task)

    return task


# PUT - Update a task
@api.put("/tasks/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for index, task in enumerate(tasks):
        if task.id == task_id:

            if updated_task.id != task_id:
                raise HTTPException(
                    status_code=400,
                    detail="Task ID mismatch"
                )

            tasks[index] = updated_task
            return updated_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )


# DELETE - Delete a task
@api.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    for index, task in enumerate(tasks):
        if task.id == task_id:
            deleted_task = tasks.pop(index)
            return deleted_task

    raise HTTPException(
        status_code=404,
        detail="Task not found"
    )