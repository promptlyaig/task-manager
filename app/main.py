from fastapi import FastAPI, HTTPException
from typing import List, Optional
from datetime import datetime
from app.models import TaskResponse, TaskStatus

# Initialize FastAPI app
app = FastAPI(
    title="Task Manager API",
    description="A simple task management API for demo purposes",
    version="1.0.0"
)

# In-memory storage
tasks_db = [
    {
        "id": 1,
        "title": "Setup project",
        "description": "Initialize FastAPI project",
        "status": TaskStatus.COMPLETED,
        "created_at": datetime(2025, 10, 1, 9, 0, 0),
        "updated_at": datetime(2025, 10, 1, 10, 0, 0)
    },
    {
        "id": 2,
        "title": "Write tests",
        "description": "Add unit tests for all endpoints",
        "status": TaskStatus.PENDING,
        "created_at": datetime(2025, 10, 2, 11, 0, 0),
        "updated_at": datetime(2025, 10, 2, 11, 0, 0)
    },
    {
        "id": 3,
        "title": "Deploy to staging",
        "description": "Deploy API to staging environment",
        "status": TaskStatus.IN_PROGRESS,
        "created_at": datetime(2025, 10, 3, 14, 30, 0),
        "updated_at": datetime(2025, 10, 3, 15, 0, 0)
    }
]

task_id_counter = 4


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to Task Manager API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "tasks": "/tasks",
            "single_task": "/tasks/{task_id}"
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "timestamp": datetime.now().isoformat()
    }


@app.get("/tasks", response_model=List[TaskResponse])
def get_tasks(status: Optional[TaskStatus] = None):
    """
    Get all tasks, optionally filtered by status
    
    Args:
        status: Filter tasks by status (pending, in_progress, completed)
    
    Returns:
        List of tasks
    """
    if status:
        filtered_tasks = [task for task in tasks_db if task["status"] == status]
        return filtered_tasks
    return tasks_db


@app.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: int):
    """
    Get a single task by ID
    
    Args:
        task_id: ID of the task to retrieve
    
    Returns:
        Task details
    
    Raises:
        HTTPException: 404 if task not found
    """
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    
    raise HTTPException(status_code=404, detail=f"Task with id {task_id} not found")


# Note: POST /tasks endpoint will be added in the PR