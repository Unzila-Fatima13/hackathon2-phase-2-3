# Phase 3: Simple Task Management Chatbot

This is a simple chatbot that understands natural language to manage tasks. It can add, delete, and mark tasks as complete using simple commands. Two versions are available: a command-line version and a web-based version.

## Features
- Natural language processing for task management
- Add tasks with natural language
- Delete tasks
- Mark tasks as complete
- View all tasks
- No API keys required
- Web interface available
- Persistent storage in JSON format

## Commands Supported
- "add task [task description]" or "add [task description]"
- "complete task [task number]" or "done [task number]"
- "delete task [task number]" or "remove [task number]"
- "show tasks" or "view tasks" or "list tasks"
- "help" or "what can you do?"

## Usage

### Command-line Version
Run `python chatbot.py` to start the command-line chatbot.

### Web Version
Run `python start_web_chatbot.py` or double-click `start_web_chatbot.bat` to start the web-based chatbot, then visit http://localhost:5001 in your browser.