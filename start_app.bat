@echo off
echo Starting Full-Stack Todo Application...

echo.
echo Starting Backend Server on port 5050...
start cmd /k "cd /d backend && python start_backend.py"

timeout /t 5 /nobreak >nul

echo.
echo Starting Frontend Server on port 3000...
start cmd /k "cd /d frontend && npx next dev"

echo.
echo Applications are starting...
echo Backend: http://localhost:5050
echo Frontend: http://localhost:3000
echo.
echo Please wait about 10-15 seconds for the servers to fully start.
echo.
echo Opening browser to frontend...
start http://localhost:3000
pause