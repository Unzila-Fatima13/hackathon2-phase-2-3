# Full-Stack Multi-User Todo Application

A modern full-stack todo application with secure authentication and user-isolated data.

## Features

- User registration and authentication
- JWT-based secure authentication
- Task management (Create, Read, Update, Delete)
- Task completion toggle
- User-specific task visibility
- Responsive web interface

## Tech Stack

### Backend
- Python 3.11+
- FastAPI
- SQLModel ORM
- Neon Serverless PostgreSQL
- JWT authentication

### Frontend
- Next.js 14+ with App Router
- TypeScript
- Tailwind CSS

## Project Structure

```
├── backend/
│   ├── src/
│   │   ├── main.py                 # FastAPI application entry point
│   │   ├── models/                 # SQLModel database models
│   │   ├── schemas/                # Pydantic request/response schemas
│   │   ├── api/                    # API route handlers
│   │   ├── database/               # Database connection and session
│   │   ├── auth/                   # Authentication utilities
│   │   └── core/                   # Core configurations
│   ├── requirements.txt            # Python dependencies
│   └── .env                        # Environment variables
├── frontend/
│   ├── src/
│   │   ├── app/                    # Next.js App Router pages
│   │   ├── components/             # React components
│   │   ├── lib/                    # Utility functions
│   │   └── styles/                 # Global styles
│   ├── package.json                # Node.js dependencies
│   ├── next.config.js              # Next.js configuration
│   └── .env.local                  # Environment variables
├── specs/                          # Feature specifications
└── README.md                       # This file
```

## Getting Started

### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables by copying `.env.example` to `.env` and configuring your settings.

4. Run the application:
   ```bash
   uvicorn src.main:app --reload
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables by creating a `.env.local` file with your API URL.

4. Run the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

All API endpoints are prefixed with `/api/`.

### Authentication
- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login a user
- `POST /api/auth/logout` - Logout a user

### Tasks
- `GET /api/tasks` - Get all tasks for the authenticated user
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{task_id}` - Get a specific task
- `PUT /api/tasks/{task_id}` - Update a specific task
- `DELETE /api/tasks/{task_id}` - Delete a specific task

## Security

- All API endpoints require JWT authentication
- User data is isolated by user ID
- Passwords are securely hashed using bcrypt
- CORS settings are configured for security

## Environment Variables

### Backend (.env)
- `DATABASE_URL` - Database connection string
- `JWT_SECRET_KEY` - Secret key for JWT signing
- `ACCESS_TOKEN_EXPIRE_MINUTES` - Access token expiration time

### Frontend (.env.local)
- `NEXT_PUBLIC_API_URL` - Backend API URL