# Vercel Deployment Guide

## Overview
This project is configured for deployment on Vercel. The frontend (Next.js application) is deployed as the main application.

## Deployment Steps

### 1. GitHub Integration
1. Push this repository to GitHub
2. Go to [Vercel Dashboard](https://vercel.com/dashboard)
3. Click "Add New Project"
4. Select your repository
5. Vercel will automatically detect the Next.js project

### 2. Build Settings (IMPORTANT)
When configuring the project in Vercel, set these exact values:
- Framework Preset: `Next.js` (will be auto-detected)
- Build Command: `cd frontend && npm run build`
- Output Directory: `frontend/.next`
- Root Directory: `.` (project root)
- Install Command: `cd frontend && npm install`

### 3. Environment Variables
Add these environment variables in the Vercel dashboard under Settings > Environment Variables:

For Production:
- `NEXT_PUBLIC_API_URL` - URL of your deployed backend API

For Preview deployments:
- `NEXT_PUBLIC_API_URL` - URL of your deployed backend API

### 4. No vercel.json Needed
This project no longer requires a `vercel.json` file for basic deployment. Vercel will handle the configuration through the dashboard settings.

## Backend API Deployment
Note: The backend API (FastAPI application in the `backend/` directory) needs to be deployed separately. Popular options include:
- Railway (https://railway.app)
- Render (https://render.com)
- AWS/Azure/GCP

Once deployed, update the `NEXT_PUBLIC_API_URL` environment variable in Vercel to point to your backend API.

## Troubleshooting

### Common Issues
1. **Build fails**: Ensure all dependencies in `frontend/package.json` are compatible
2. **Environment variables missing**: Verify all required env vars are set in Vercel dashboard
3. **API calls failing**: Check that `NEXT_PUBLIC_API_URL` points to the correct backend URL
4. **Build Command error**: Make sure you're using `cd frontend && npm run build` as the build command
5. **Output Directory error**: Ensure you're using `frontend/.next` as the output directory

### Verifying Deployment
After deployment, check:
1. The frontend loads correctly
2. API calls to the backend work as expected
3. Authentication and task operations function properly