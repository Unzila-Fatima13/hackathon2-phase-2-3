import uvicorn
import os
import sys
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = str(Path(__file__).parent)
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Change to the backend directory to ensure proper module resolution
os.chdir(backend_dir)

if __name__ == "__main__":
    print("Starting backend server on http://localhost:5050")
    print("Available endpoints:")
    print("- GET / - Welcome message")
    print("- GET /health - Health check")
    print("- POST /api/auth/register - User registration")
    print("- POST /api/auth/login - User login")
    print("- POST /api/auth/logout - User logout")
    print("- GET /api/tasks - Get user tasks")
    print("- POST /api/tasks - Create task")
    print("- GET /api/tasks/{id} - Get specific task")
    print("- PUT /api/tasks/{id} - Update task")
    print("- DELETE /api/tasks/{id} - Delete task")
    uvicorn.run("src.main:app", host="0.0.0.0", port=5050, reload=False)