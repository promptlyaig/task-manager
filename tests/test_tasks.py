import pytest
from fastapi.testclient import TestClient
from app.main import app

# Create test client
client = TestClient(app)


class TestHealthEndpoint:
    """Tests for health check endpoint"""
    
    def test_health_check(self):
        """Test health endpoint returns correct status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data
        assert "timestamp" in data


class TestGetTasks:
    """Tests for GET /tasks endpoint"""
    
    def test_get_all_tasks(self):
        """Test getting all tasks"""
        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
    def test_get_tasks_with_status_filter(self):
        """Test filtering tasks by status"""
        response = client.get("/tasks?status=pending")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # All returned tasks should have status 'pending'
        for task in data:
            assert task["status"] == "pending"
    
    def test_get_tasks_schema(self):
        """Test that tasks have correct schema"""
        response = client.get("/tasks")
        assert response.status_code == 200
        data = response.json()
        
        # Check first task has all required fields
        if len(data) > 0:
            task = data[0]
            assert "id" in task
            assert "title" in task
            assert "status" in task
            assert "created_at" in task
            assert "updated_at" in task


class TestGetSingleTask:
    """Tests for GET /tasks/{task_id} endpoint"""
    
    def test_get_existing_task(self):
        """Test getting an existing task by ID"""
        response = client.get("/tasks/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert "title" in data
        assert "status" in data
    
    def test_get_nonexistent_task(self):
        """Test getting a task that doesn't exist"""
        response = client.get("/tasks/9999")
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data


# Note: Tests for POST /tasks will be added when the endpoint is implemented
