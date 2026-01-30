# Phase 3: Enhanced Todo Application with Natural Language Processing

## Overview

This directory contains the organized Phase 3 implementation of the full-stack todo application with integrated task chatbot functionality. The architecture maintains the existing API and authentication functionality while adding natural language processing capabilities.

## Structure

```
phase3_new/
├── frontend/                 # Next.js frontend application
│   ├── src/
│   │   ├── app/             # App Router pages
│   │   ├── components/      # Reusable UI components
│   │   ├── lib/            # API and auth utilities
│   │   └── styles/         # Global styles
│   └── package.json
└── backend/                 # FastAPI backend application
    ├── api/                # API route definitions
    │   ├── auth.py         # Authentication endpoints
    │   ├── tasks.py        # Task management endpoints
    │   └── chatbot.py      # Natural language chatbot endpoints
    ├── services/           # Business logic
    │   ├── task_service.py # Task operations
    │   ├── user_service.py # User operations
    │   └── task_chatbot.py # Chatbot logic with database integration
    ├── models/             # Database models
    ├── auth/               # Authentication handlers
    ├── database/           # Database configuration
    ├── core/               # Core configurations
    ├── src/
    │   └── main.py         # Main application entry point
    ├── requirements.txt
    └── run_server.py       # Server startup script
```

## Features

### Backend
- **FastAPI** backend with proper authentication
- **SQLModel** for database operations
- **Natural Language Processing** for task management
- **JWT-based authentication** system
- **User-isolated task management**

### Frontend
- **Next.js 14** with App Router
- **TypeScript** for type safety
- **Tailwind CSS** for styling
- **Integrated chatbot** component with natural language support
- **Responsive design** for various screen sizes

### Chatbot Capabilities
The task chatbot supports natural language commands:

#### Adding Tasks
- `add task Buy groceries`
- `add Buy milk and bread`
- `create task Finish report`

#### Managing Tasks
- `show tasks` or `list tasks` - Show all tasks
- `complete task 1` or `done 1` - Mark task as complete by ID
- `complete task Buy groceries` or `done Buy groceries` - Mark task as complete by name
- `delete task 2` or `remove 2` - Delete task by ID
- `delete task Buy groceries` or `remove Buy groceries` - Delete task by name

#### Help
- `help` - Show available commands

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login user
- `POST /api/auth/logout` - Logout user
- `GET /api/auth/me` - Get current user info
- `POST /api/auth/refresh` - Refresh access token

### Tasks
- `GET /api/tasks` - Get all tasks for current user
- `POST /api/tasks` - Create new task
- `PUT /api/tasks/{id}` - Update task
- `DELETE /api/tasks/{id}` - Delete task

### Chatbot
- `POST /api/chatbot/chat` - Chat with the task management bot
- `GET /api/chatbot/tasks` - Get user tasks via chatbot
- `POST /api/chatbot/reset` - Reset user's chatbot instance

## Setup Instructions

### Backend Setup
1. Navigate to the backend directory:
   ```bash
   cd phase3_new/backend
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables in `.env`:
   ```
   DATABASE_URL=sqlite:///./todo_app.db
   SECRET_KEY=your-secret-key-here
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   REFRESH_TOKEN_EXPIRE_DAYS=7
   BACKEND_CORS_ORIGINS=http://localhost:3000
   ```

4. Initialize the database:
   ```bash
   python initialize_db.py
   ```

5. Start the backend server:
   ```bash
   python run_server.py
   ```

### Frontend Setup
1. Navigate to the frontend directory:
   ```bash
   cd phase3_new/frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables in `.env.local`:
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. Start the development server:
   ```bash
   npm run dev
   ```

## Usage

1. Open your browser and go to `http://localhost:3000`
2. Register a new account or log in with an existing one
3. Access the dashboard at `/dashboard`
4. Use the chatbot panel to manage tasks with natural language commands
5. Alternatively, use the traditional task form and list

## Architecture Notes

The Phase 3 implementation maintains backward compatibility with the existing API while adding natural language processing capabilities. The chatbot integrates seamlessly with the existing authentication and database systems, ensuring user data isolation and security.

## Error Handling

The application includes comprehensive error handling:
- Network error detection and retry logic
- Authentication error handling with token refresh
- Proper error messages for API failures
- User-friendly error displays

## Security

- JWT-based authentication with refresh tokens
- Password hashing using bcrypt
- SQL injection protection through parameterized queries
- CORS configuration for secure cross-origin requests
- Rate limiting considerations (can be added as needed)