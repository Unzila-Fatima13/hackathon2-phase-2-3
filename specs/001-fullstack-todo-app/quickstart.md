# Quickstart Guide: Full-Stack Multi-User Todo Application

## Prerequisites

- Node.js 18+ (for Next.js frontend)
- Python 3.11+ (for FastAPI backend)
- PostgreSQL-compatible database (Neon Serverless PostgreSQL)
- Git

## Environment Setup

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```

3. Install backend dependencies:
   ```
   cd ../backend
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create `.env` files in both frontend and backend directories:

   **Frontend (.env):**
   ```
   NEXT_PUBLIC_API_URL=http://localhost:8000
   NEXTAUTH_SECRET=your-secret-key
   NEXTAUTH_URL=http://localhost:3000
   ```

   **Backend (.env):**
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/todoapp
   JWT_SECRET=your-jwt-secret
   JWT_ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   ```

## Database Setup

1. Set up Neon Serverless PostgreSQL database
2. Run database migrations:
   ```
   cd backend
   alembic upgrade head
   ```

## Running the Application

### Development Mode

1. Start the backend server:
   ```
   cd backend
   uvicorn main:app --reload --port 8000
   ```

2. In a new terminal, start the frontend:
   ```
   cd frontend
   npm run dev
   ```

3. Access the application at `http://localhost:3000`

### Production Build

1. Build the frontend:
   ```
   cd frontend
   npm run build
   ```

2. Run the backend:
   ```
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

## Key Technologies Used

- **Frontend**: Next.js 16+ with App Router, TypeScript, Tailwind CSS
- **Backend**: Python FastAPI with SQLModel ORM
- **Database**: Neon Serverless PostgreSQL
- **Authentication**: Better Auth with JWT tokens
- **Deployment**: Docker containerization ready

## API Endpoints

- Authentication: `POST /api/auth/login`, `POST /api/auth/register`
- Tasks: `GET /api/tasks`, `POST /api/tasks`, `PUT /api/tasks/{id}`, `DELETE /api/tasks/{id}`
- All API endpoints are protected with JWT authentication

## Testing

### Frontend Testing
```
npm run test
```

### Backend Testing
```
pytest
```

## Troubleshooting

1. **Database Connection Issues**: Verify your Neon PostgreSQL connection string is correct
2. **Authentication Failures**: Ensure JWT secrets match between frontend and backend
3. **CORS Issues**: Check that your frontend URL is properly configured in the backend CORS settings