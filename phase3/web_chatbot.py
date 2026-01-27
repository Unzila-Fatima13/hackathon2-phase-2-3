from flask import Flask, render_template_string, request, jsonify
import json
import os
import re
from datetime import datetime

app = Flask(__name__)

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

    def get_tasks_json(self):
        """Return tasks in JSON format"""
        return self.tasks

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

# Initialize the chatbot
bot = TaskChatbot()

@app.route('/')
def index():
    html_template = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Task Management Chatbot</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .chat-container {
                background-color: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                height: 500px;
                display: flex;
                flex-direction: column;
            }
            .chat-messages {
                flex: 1;
                overflow-y: auto;
                margin-bottom: 15px;
                padding: 10px;
                background-color: #fafafa;
                border-radius: 5px;
            }
            .message {
                margin: 10px 0;
                padding: 8px;
            }
            .user-message {
                background-color: #dcf8c6;
                text-align: right;
                border-radius: 10px 0 10px 10px;
            }
            .bot-message {
                background-color: #e5e5ea;
                border-radius: 0 10px 10px 10px;
            }
            .input-container {
                display: flex;
                gap: 10px;
            }
            #user-input {
                flex: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
                font-size: 16px;
            }
            #send-btn {
                padding: 10px 20px;
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            #send-btn:hover {
                background-color: #45a049;
            }
            .task-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 8px;
                margin: 5px 0;
                background-color: #f0f0f0;
                border-radius: 5px;
            }
            .task-completed {
                text-decoration: line-through;
                color: gray;
            }
            h1 {
                text-align: center;
                color: #333;
            }
            .help-text {
                font-size: 12px;
                color: #666;
                text-align: center;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <h1>Task Management Chatbot</h1>
        <div class="chat-container">
            <div id="chat-messages" class="chat-messages">
                <div class="message bot-message">
                    Hello! I'm your task management assistant. Type 'help' to see what I can do.
                </div>
            </div>
            <div class="input-container">
                <input type="text" id="user-input" placeholder="Type your command..." onkeypress="handleKeyPress(event)">
                <button id="send-btn" onclick="sendMessage()">Send</button>
            </div>
            <div class="help-text">
                Examples: "add task Buy groceries", "show tasks", "done 1", "delete task 2"
            </div>
        </div>

        <script>
            function sendMessage() {
                const inputElement = document.getElementById('user-input');
                const message = inputElement.value.trim();

                if (message === '') return;

                // Display user message
                addMessage(message, 'user');
                inputElement.value = '';

                // Send to server
                fetch('/chat', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({message: message})
                })
                .then(response => response.json())
                .then(data => {
                    addMessage(data.response, 'bot');

                    // If it's a task list command, also update the task display
                    if (message.toLowerCase().includes('show') || message.toLowerCase().includes('list') || message.toLowerCase().includes('view')) {
                        updateTaskDisplay();
                    }
                })
                .catch(error => {
                    addMessage('Error: Could not connect to server', 'bot');
                });
            }

            function addMessage(message, sender) {
                const chatMessages = document.getElementById('chat-messages');
                const messageDiv = document.createElement('div');
                messageDiv.classList.add('message');
                messageDiv.classList.add(sender === 'user' ? 'user-message' : 'bot-message');
                messageDiv.textContent = message;
                chatMessages.appendChild(messageDiv);
                chatMessages.scrollTop = chatMessages.scrollHeight;
            }

            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }

            function updateTaskDisplay() {
                fetch('/tasks')
                .then(response => response.json())
                .then(data => {
                    // We'll update the display with tasks, but for now just refresh if needed
                });
            }
        </script>
    </body>
    </html>
    '''
    return render_template_string(html_template)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message', '')
    response = bot.parse_command(user_message)
    return jsonify({'response': response})

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(bot.get_tasks_json())

if __name__ == '__main__':
    app.run(debug=True, port=5001)