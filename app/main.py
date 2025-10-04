from fastapi import FastAPI, HTTPException
from typing import List, Optional
from datetime import datetime
from app.models import TaskResponse, TaskStatus, TaskCreate

# Initialize FastAPI app
app = FastAPI(
    title="Task Manager API",
    description="A simple task management API for demo purposes",
    version="1.0.0"
)

# In-memory storage with course-related tasks
tasks_db = [
    {
        "id": 1,
        "title": "Introduction_to_LLMs",
        "description": "Learn fundamentals of Large Language Models",
        "status": TaskStatus.COMPLETED,
        "created_at": datetime(2025, 9, 1, 9, 0, 0),
        "updated_at": datetime(2025, 9, 5, 17, 30, 0)
    },
    {
        "id": 2,
        "title": "Python_Essentials",
        "description": "Master Python basics for AI development",
        "status": TaskStatus.COMPLETED,
        "created_at": datetime(2025, 9, 6, 10, 0, 0),
        "updated_at": datetime(2025, 9, 10, 16, 0, 0)
    },
    {
        "id": 3,
        "title": "pdf_processing",
        "description": "Learn document processing techniques",
        "status": TaskStatus.COMPLETED,
        "created_at": datetime(2025, 9, 11, 11, 0, 0),
        "updated_at": datetime(2025, 9, 15, 14, 30, 0)
    },
    {
        "id": 4,
        "title": "LangChain_basics",
        "description": "Introduction to LangChain framework",
        "status": TaskStatus.PENDING,
        "created_at": datetime(2025, 9, 16, 9, 0, 0),
        "updated_at": datetime(2025, 9, 16, 9, 0, 0)
    },
    {
        "id": 5,
        "title": "Langgraph-Basics",
        "description": "Fundamentals of LangGraph for agent workflows",
        "status": TaskStatus.COMPLETED,
        "created_at": datetime(2025, 9, 20, 10, 30, 0),
        "updated_at": datetime(2025, 9, 25, 15, 0, 0)
    },
    {
        "id": 6,
        "title": "Langgraph-Explore",
        "description": "Deep dive into advanced LangGraph concepts",
        "status": TaskStatus.IN_PROGRESS,
        "created_at": datetime(2025, 9, 26, 9, 0, 0),
        "updated_at": datetime(2025, 10, 3, 14, 30, 0)
    },
    {
        "id": 7,
        "title": "OrderingAgent",
        "description": "Build an ordering agent using LangGraph",
        "status": TaskStatus.PENDING,
        "created_at": datetime(2025, 10, 1, 10, 0, 0),
        "updated_at": datetime(2025, 10, 1, 10, 0, 0)
    },
    {
        "id": 8,
        "title": "DeliveryAgent",
        "description": "Implement a delivery tracking agent",
        "status": TaskStatus.PENDING,
        "created_at": datetime(2025, 10, 1, 10, 15, 0),
        "updated_at": datetime(2025, 10, 1, 10, 15, 0)
    },
    {
        "id": 9,
        "title": "MultiAgent-DataShare",
        "description": "Build multi-agent system with shared data",
        "status": TaskStatus.PENDING,
        "created_at": datetime(2025, 10, 1, 10, 30, 0),
        "updated_at": datetime(2025, 10, 1, 10, 30, 0)
    },
    {
        "id": 10,
        "title": "MCP-Helloworld",
        "description": "Create first Model Context Protocol application",
        "status": TaskStatus.PENDING,
        "created_at": datetime(2025, 10, 1, 10, 45, 0),
        "updated_at": datetime(2025, 10, 1, 10, 45, 0)
    }
]

task_id_counter = 11


@app.get("/")
def read_root():
    """Root endpoint"""
    return {
        "message": "Welcome to Task Manager API - Course Progress Tracker",
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

# ============================================================================
# BUGGY POST ENDPOINT - Added in PR (has multiple issues)
# ============================================================================

@app.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    """
    Create a new task
    
    Args:
        task: Task data from request body
    
    Returns:
        Created task with ID and timestamps
    
    NOTE: This implementation has several bugs that need to be fixed:
    - BUG 1: Missing validation - allows empty title
    - BUG 2: Missing validation - allows invalid status values  
    - BUG 3: Doesn't set default status to "pending" when status is None
    - BUG 4: No error handling for database operations
    """
    global task_id_counter
    
    # BUG 1: No validation for empty title
    # Should check: if not task.title or not task.title.strip()
    
    # BUG 2: No validation for invalid status values
    # The status field accepts the string directly without validation
    
    # BUG 3: Wrong default status handling
    # When status is None, it should default to "pending" but doesn't
    current_time = datetime.now()
    
    new_task = {
        "id": task_id_counter,
        "title": task.title,  # BUG 1: Allows empty strings
        "description": task.description,
        "status": task.status,  # BUG 3: Can be None, should default to "pending"
        "created_at": current_time,
        "updated_at": current_time
    }
    
    # BUG 4: No try-except for potential errors
    tasks_db.append(new_task)
    task_id_counter += 1
    
    return new_task
