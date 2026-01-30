@echo off
echo Starting Phase 3 Todo Application...

REM Start the backend server in a new window
start cmd /k "cd /d phase3_new\backend && python run_server.py"

REM Wait a moment for the backend to start
timeout /t 3 /nobreak >nul

REM Start the frontend in a new window
start cmd /k "cd /d phase3_new\frontend && npm run dev"

echo Phase 3 application started!
echo Backend will be available at http://localhost:8000
echo Frontend will be available at http://localhost:3000
pause