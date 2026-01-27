import json
import os
import re
from datetime import datetime

class TaskChatbot:
    def __init__(self):
        self.tasks_file = "tasks.json"
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.tasks_file):
            with open(self.tasks_file, 'r') as f:
                self.tasks = json.load(f)
        else:
            self.tasks = []

    def save_tasks(self):
        """Save tasks to JSON file"""
        with open(self.tasks_file, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, description):
        """Add a new task"""
        task = {
            "id": len(self.tasks) + 1,
            "description": description.strip(),
            "completed": False,
            "created_at": datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
        return f"Added task: '{description}'"

    def delete_task(self, task_id):
        """Delete a task by ID"""
        for i, task in enumerate(self.tasks):
            if task['id'] == int(task_id):
                deleted_task = self.tasks.pop(i)
                # Renumber remaining tasks
                for j in range(i, len(self.tasks)):
                    self.tasks[j]['id'] = j + 1
                self.save_tasks()
                return f"Deleted task: '{deleted_task['description']}'"
        return f"Task with ID {task_id} not found"

    def complete_task(self, task_id):
        """Mark a task as complete"""
        for task in self.tasks:
            if task['id'] == int(task_id):
                task['completed'] = True
                self.save_tasks()
                return f"Completed task: '{task['description']}'"
        return f"Task with ID {task_id} not found"

    def list_tasks(self):
        """List all tasks"""
        if not self.tasks:
            return "No tasks found. Add some tasks!"

        response = "Your tasks:\n"
        for task in self.tasks:
            status = "✓" if task['completed'] else "○"
            response += f"{status} [{task['id']}] {task['description']}\n"
        return response

    def parse_command(self, user_input):
        """Parse natural language command"""
        user_input = user_input.lower().strip()

        # Add task commands
        if any(word in user_input for word in ['add task', 'add a task', 'add', 'create task', 'new task']):
            # Extract task description after the command
            for prefix in ['add task ', 'add a task ', 'add ', 'create task ', 'new task ']:
                if prefix in user_input:
                    description = user_input.split(prefix, 1)[1]
                    return self.add_task(description)

            # If no prefix matched, try to get everything after 'add'
            if 'add' in user_input:
                parts = user_input.split('add', 1)
                if len(parts) > 1:
                    description = parts[1].strip()
                    return self.add_task(description)

        # Complete/done task commands
        if any(word in user_input for word in ['complete task', 'complete', 'done task', 'done', 'finish task', 'finish']):
            # Extract task number
            numbers = re.findall(r'\d+', user_input)
            if numbers:
                task_id = numbers[0]
                return self.complete_task(task_id)
            return "Please specify which task number to complete."

        # Delete/remove task commands
        if any(word in user_input for word in ['delete task', 'delete', 'remove task', 'remove']):
            # Extract task number
            numbers = re.findall(r'\d+', user_input)
            if numbers:
                task_id = numbers[0]
                return self.delete_task(task_id)
            return "Please specify which task number to delete."

        # List tasks commands
        if any(word in user_input for word in ['show tasks', 'view tasks', 'list tasks', 'my tasks', 'all tasks', 'tasks']):
            return self.list_tasks()

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
        """Run the chatbot"""
        print("Task Management Chatbot")
        print("Type 'quit' or 'exit' to stop")
        print("Type 'help' to see available commands")
        print("-" * 40)

        while True:
            user_input = input("\nYou: ").strip()

            if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
                print("Chatbot: Goodbye! Have a great day!")
                break

            if not user_input:
                print("Chatbot: Please enter a command.")
                continue

            response = self.parse_command(user_input)
            print(f"Chatbot: {response}")

if __name__ == "__main__":
    bot = TaskChatbot()
    bot.run()