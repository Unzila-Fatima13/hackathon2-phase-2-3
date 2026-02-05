@echo off
REM Vercel Setup Script
REM Use this script to prepare your project for Vercel deployment

echo Preparing project for Vercel deployment...

echo 1. Checking frontend directory...
if not exist "frontend" (
    echo ERROR: Frontend directory not found!
    exit /b 1
)

echo 2. Checking frontend package.json...
if not exist "frontend\package.json" (
    echo ERROR: Frontend package.json not found!
    exit /b 1
)

echo 3. Validating frontend build...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo WARNING: npm install failed, but continuing...
)

npm run build
if %errorlevel% neq 0 (
    echo ERROR: Frontend build failed!
    cd ..
    exit /b %errorlevel%
)

echo 4. Build successful! Returning to root...
cd ..

echo 5. Project is ready for Vercel deployment!
echo.
echo To deploy to Vercel:
echo   1. Push this repository to GitHub
echo   2. Import the project in Vercel dashboard
echo   3. Set Build Command to: "cd frontend && npm run build"
echo   4. Set Output Directory to: "frontend/.next"
echo   5. Set Root Directory to: "."
echo.
echo Remember to set NEXT_PUBLIC_API_URL environment variable in Vercel dashboard.