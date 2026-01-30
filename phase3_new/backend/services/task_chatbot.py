import json
import os
import re
from datetime import datetime
from sqlmodel import Session, select
from typing import List, Dict, Any

from models.task import Task
from models.user import User


class TaskChatbot:
    def __init__(self, user_id: str = None):
        self.user_id = user_id

    def get_user_tasks(self, session: Session, user_id: str) -> List[Dict[str, Any]]:
        """Get tasks for a specific user from the database"""
        from services.task_service import TaskService

        # Get tasks using TaskService
        tasks = TaskService.get_tasks_for_user(session=session, user_id=user_id)

        # Convert to the format expected by the chatbot
        formatted_tasks = []
        for i, task in enumerate(tasks):
            formatted_tasks.append({
                "id": i + 1,  # Sequential numbering for chatbot
                "original_id": task.id,  # Actual DB ID
                "description": task.title,  # Using title instead of description
                "completed": task.is_completed,  # Using is_completed field
                "created_at": task.created_at.isoformat() if task.created_at else datetime.now().isoformat()
            })
        return formatted_tasks

    def add_task(self, description: str, session: Session, user_id: str):
        """Add a new task to the database for the user"""
        from services.task_service import TaskService
        from models.task import TaskCreate

        # Create the task in the database using TaskService
        task_create = TaskCreate(title=description.strip(), description=description.strip())
        new_task = TaskService.create_task(session=session, task_create=task_create, user_id=user_id)

        return f"Added task: '{description.strip()}'"

    def delete_task(self, task_id: str, session: Session, user_id: str):
        """Delete a task by ID from the database"""
        from services.task_service import TaskService
        import uuid

        # Get all user tasks to map sequential ID to actual DB ID
        all_tasks = TaskService.get_tasks_for_user(session=session, user_id=user_id)

        # Find the task with the specified sequential position
        try:
            task_position = int(task_id) - 1  # Convert to 0-based index
            if 0 <= task_position < len(all_tasks):
                task_to_delete = all_tasks[task_position]
                # Delete the task from the database
                TaskService.delete_task(session=session, task_id=task_to_delete.id, user_id=user_id)
                return f"Deleted task: '{task_to_delete.title}'"
            else:
                return f"Task with ID {task_id} not found"
        except ValueError:
            return f"Invalid task ID: {task_id}"

    def complete_task(self, task_id: str, session: Session, user_id: str):
        """Mark a task as complete in the database"""
        from services.task_service import TaskService
        from models.task import TaskUpdate
        import uuid

        # Get all user tasks to map sequential ID to actual DB ID
        all_tasks = TaskService.get_tasks_for_user(session=session, user_id=user_id)

        try:
            task_position = int(task_id) - 1  # Convert to 0-based index
            if 0 <= task_position < len(all_tasks):
                task_to_complete = all_tasks[task_position]
                # Update the task in the database using TaskService
                task_update = TaskUpdate(is_completed=True)
                updated_task = TaskService.update_task(session=session, task_id=task_to_complete.id,
                                                     task_update=task_update, user_id=user_id)
                return f"Completed task: '{task_to_complete.title}'"
            else:
                return f"Task with ID {task_id} not found"
        except ValueError:
            return f"Invalid task ID: {task_id}"

    def list_tasks(self, session: Session, user_id: int):
        """List all tasks for the user"""
        tasks = self.get_user_tasks(session, user_id)

        if not tasks:
            return "No tasks found. Add some tasks!"

        response = "Your tasks:\n"
        for task in tasks:
            status = "✓" if task['completed'] else "○"
            response += f"{status} [{task['id']}] {task['description']}\n"
        return response

    def parse_command(self, user_input, session: Session, user_id: int):
        """Parse natural language command"""
        user_input = user_input.lower().strip()

        # Add task commands
        if any(word in user_input for word in ['add task', 'add a task', 'add', 'create task', 'new task']):
            # Extract task description after the command
            for prefix in ['add task ', 'add a task ', 'add ', 'create task ', 'new task ']:
                if prefix in user_input:
                    description = user_input.split(prefix, 1)[1]
                    return self.add_task(description, session, user_id)

            # If no prefix matched, try to get everything after 'add'
            if 'add' in user_input:
                parts = user_input.split('add', 1)
                if len(parts) > 1:
                    description = parts[1].strip()
                    return self.add_task(description, session, user_id)

        # Complete/done task commands
        if any(word in user_input for word in ['complete task', 'complete', 'done task', 'done', 'finish task', 'finish']):
            # Extract task number
            numbers = re.findall(r'\d+', user_input)
            if numbers:
                task_id = numbers[0]
                return self.complete_task(task_id, session, user_id)
            return "Please specify which task number to complete."

        # Delete/remove task commands
        if any(word in user_input for word in ['delete task', 'delete', 'remove task', 'remove']):
            # Extract task number
            numbers = re.findall(r'\d+', user_input)
            if numbers:
                task_id = numbers[0]
                return self.delete_task(task_id, session, user_id)
            return "Please specify which task number to delete."

        # List tasks commands
        if any(word in user_input for word in ['show tasks', 'view tasks', 'list tasks', 'my tasks', 'all tasks', 'tasks']):
            return self.list_tasks(session, user_id)

        # Help commands
        if any(word in user_input for word in ['help', 'what can you do', 'commands', 'what can i do']):
            return (
                "I can help you manage tasks!\n\n"
                "Commands I understand:\n"
                "- 'add task [description]' or 'add [description]' to add a task\n"
                "- 'complete task [number]' or 'done [number]' to mark as complete\n"
                "- 'delete task [number]' or 'remove [number]' to delete a task\n"
                "- 'show tasks' or 'list tasks' to view all tasks\n"
                "- 'help' to show this message"
            )

        # Default response
        return "I didn't understand that command. Type 'help' to see what I can do."

    def run(self):
        """Run the chatbot (CLI version - for testing only)"""
        print("Task Management Chatbot - CLI Mode (Testing Only)")
        print("Note: This CLI version doesn't connect to the database.")
        print("For production use, use the API endpoints with proper session and user_id.")
        print("Type 'quit' or 'exit' to stop")
        print("Type 'help' to see available commands")
        print("-" * 40)

        # For CLI mode, we'll simulate a dummy session and user
        class DummySession:
            def exec(self, statement):
                return []

        dummy_session = DummySession()
        dummy_user_id = 1  # For testing only

        while True:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("Chatbot: Goodbye! Have a great day!")
                break

            if not user_input:
                print("Chatbot: Please enter a command.")
                continue

            # For CLI mode, we'll catch the error if database is needed
            try:
                response = self.parse_command(user_input, dummy_session, dummy_user_id)
            except Exception as e:
                response = f"Command requires database connection: {str(e)}"

            print(f"Chatbot: {response}")

if __name__ == "__main__":
    bot = TaskChatbot()
    bot.run()