# Instructions for Phase 3 Task Chatbot

## How to Run the Chatbot

### Command-line Version

#### Method 1: Direct Python execution
```bash
cd phase3
python chatbot.py
```

#### Method 2: Using the batch file (Windows)
Double-click on `run_chatbot.bat` or run:
```bash
run_chatbot.bat
```

### Web Version (Now Showing in Browser!)

#### Method 1: Direct Python execution
```bash
cd phase3
python start_web_chatbot.py
```

#### Method 2: Using the batch file (Windows)
Double-click on `start_web_chatbot.bat` or run:
```bash
start_web_chatbot.bat
```

Then visit http://localhost:5001 in your browser to interact with the chatbot!

The web version provides a visual interface where you can:
- Type commands in the input box
- See chat history
- View tasks in a list format
- Interact with the chatbot through a modern UI

## Available Commands

### Adding Tasks
- "add task Buy groceries"
- "add Walk the dog"
- "create task Finish homework"
- "new task Call mom"

### Completing Tasks
- "complete task 1"
- "done 1"
- "finish task 2"

### Deleting Tasks
- "delete task 1"
- "remove task 1"

### Viewing Tasks
- "show tasks"
- "view tasks"
- "list tasks"
- "my tasks"

### Getting Help
- "help"
- "what can you do?"

## Example Session

You: add task Buy milk
Chatbot: Added task: 'Buy milk'

You: add task Call doctor
Chatbot: Added task: 'Call doctor'

You: show tasks
Chatbot: Your tasks:
○ [1] Buy milk
○ [2] Call doctor

You: done 1
Chatbot: Completed task: 'Buy milk'

You: show tasks
Chatbot: Your tasks:
✓ [1] Buy milk
○ [2] Call doctor

## Notes
- Tasks are saved in tasks.json file
- Task numbers are automatically managed
- The chatbot works offline with no internet connection required
- Type 'quit' or 'exit' to stop the chatbot