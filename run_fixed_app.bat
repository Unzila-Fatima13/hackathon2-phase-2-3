@echo off
echo ===============================================
echo Starting Fixed Full-Stack Todo Application
echo ===============================================

echo.
echo STOPPING any existing processes on ports 8000 and 3000...
for /f "skip=3 tokens=5" %%a in ('netstat -ano ^| findstr :8000 ^| findstr LISTENING') do taskkill /PID %%a /F 2>nul
for /f "skip=3 tokens=5" %%a in ('netstat -ano ^| findstr :3000 ^| findstr LISTENING') do taskkill /PID %%a /F 2>nul

echo.
echo CLEARING frontend cache...
rd /s /q frontend\node_modules 2>nul
rd /s /q frontend\.next 2>nul

echo.
echo INSTALLING frontend dependencies...
cd frontend
npm install
if %errorlevel% neq 0 (
  echo Failed to install frontend dependencies
  pause
  exit /b %errorlevel%
)

echo.
echo RETURNING to main directory...
cd ..

echo.
echo Starting Backend Server on port 8000...
start "Backend" cmd /k "cd backend && python start_backend.py"

echo Waiting for backend to start...
timeout /t 10 /nobreak >nul

echo.
echo Starting Frontend Server on port 3000...
start "Frontend" cmd /k "cd frontend && npx next dev"

echo.
echo ===============================================
echo APPLICATION STARTED SUCCESSFULLY!
echo ===============================================
echo.
echo BACKEND: http://localhost:5050
echo    - Health check: http://localhost:5050/health
echo    - API docs: http://localhost:5050/docs
echo.
echo FRONTEND: http://localhost:3000
echo    - Register: http://localhost:3000/register
echo    - Login: http://localhost:3000/login
echo    - Dashboard: http://localhost:3000/dashboard
echo.
echo Please wait 15-20 seconds for everything to load.
echo.
echo Opening browser to frontend...
start http://localhost:3000
echo.
pause