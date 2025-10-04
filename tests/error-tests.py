# Start the server
uvicorn app.main:app --reload

# Test 1: Create task with empty title (should fail but doesn't)
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "", "description": "Test"}'

# Test 2: Create task with invalid status (should fail but doesn't)
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "status": "invalid_status"}'

# Test 3: Create task without status (should default to "pending" but becomes null)
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Task", "description": "No status provided"}'

