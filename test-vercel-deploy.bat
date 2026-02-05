@echo off
REM Vercel Deployment Test Script

echo Testing build process for Vercel deployment...

echo Installing frontend dependencies...
cd frontend
npm install
if %errorlevel% neq 0 (
    echo Failed to install frontend dependencies
    exit /b %errorlevel%
)

echo Building frontend application...
npm run build
if %errorlevel% neq 0 (
    echo Frontend build failed
    exit /b %errorlevel%
)

echo Build completed successfully!
echo The application is ready for Vercel deployment.
echo Please ensure your NEXT_PUBLIC_API_URL environment variable is set in Vercel dashboard.