# Get all completed course modules
curl http://localhost:8000/tasks?status=completed

# Get pending modules
curl http://localhost:8000/tasks?status=pending

# Get current module in progress
curl http://localhost:8000/tasks?status=in_progress

# Get specific module
curl http://localhost:8000/tasks/6

