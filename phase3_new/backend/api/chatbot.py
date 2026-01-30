from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Dict, Any

from database.database import get_session
from services.task_chatbot import TaskChatbot
from auth.auth_handler import get_current_user
from models.user import User

router = APIRouter(
    prefix="/chatbot",
    tags=["chatbot"]
)

# Global chatbot instance (in production, you'd want per-user instances)
chatbot_instances: Dict[int, TaskChatbot] = {}

def get_user_chatbot(user_id: int) -> TaskChatbot:
    """Get or create a chatbot instance for a specific user"""
    if user_id not in chatbot_instances:
        chatbot_instances[user_id] = TaskChatbot(user_id=user_id)
    return chatbot_instances[user_id]

@router.post("/chat")
async def chat_with_bot(
    message: str,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Chat with the task management bot using natural language
    """
    try:
        user_chatbot = get_user_chatbot(current_user.id)
        response = user_chatbot.parse_command(message, session, current_user.id)
        return {"response": response, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat command: {str(e)}")

@router.get("/tasks")
async def get_user_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get tasks for the current user through the chatbot
    """
    try:
        user_chatbot = get_user_chatbot(current_user.id)
        tasks = user_chatbot.get_user_tasks(session, current_user.id)
        return {"tasks": tasks, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving tasks: {str(e)}")

@router.post("/reset")
async def reset_user_chatbot(
    current_user: User = Depends(get_current_user)
):
    """
    Reset the chatbot instance for the current user
    """
    if current_user.id in chatbot_instances:
        del chatbot_instances[current_user.id]
    return {"message": "Chatbot reset successfully", "success": True}