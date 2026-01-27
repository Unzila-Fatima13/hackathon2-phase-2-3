---
id: 8
title: Enhanced Task Operations by Name
stage: general
date: 2026-01-27
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-fullstack-todo-app
user: m.anas
command: ''
labels: [task, chatbot, enhancement, operations, name]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - phase3/task_manager.py
 - phase3/chatbot.py
 - phase3/web_chatbot.py
tests:
 - phase3/test_task_operations_by_name.py
---

## Prompt

Enhance the task chatbot to support task operations by name in addition to by number. The chatbot should allow users to complete and delete tasks using partial names instead of requiring exact task numbers. Additionally, display actual database task IDs when listing tasks instead of sequential indexes. This improvement makes the chatbot more user-friendly by allowing natural language interactions with tasks.

## Response snapshot

Enhanced the task chatbot to support task operations by name in addition to by number. The implementation includes:

- Modified task_manager.py to add functions for finding tasks by partial name matches
- Updated chatbot.py and web_chatbot.py to handle name-based task operations
- Changed task listing to show actual database IDs instead of sequential indexes
- Added fuzzy matching algorithm to find tasks by partial name matches
- Maintained backward compatibility with number-based operations
- Improved user experience with clearer feedback messages

The chatbot now supports commands like "complete grocery shopping" or "delete meeting" using partial name matching, while still supporting traditional number-based operations.

## Outcome

- ✅ Impact: Improved user experience by enabling name-based task operations alongside traditional number-based operations
- 🧪 Tests: Created comprehensive tests for name-based task operations and partial matching
- 📁 Files: Modified 3 core files to add name-based task operations functionality
- 🔁 Next prompts: Users can now interact with tasks using either names or numbers
- 🧠 Reflection: Name-based operations significantly enhance usability and natural interaction

## Evaluation notes (flywheel)

- Failure modes observed: None identified in initial testing; proper error handling implemented for ambiguous name matches
- Graders run and results (PASS/FAIL): All tests pass, confirming both name and number-based operations work correctly
- Prompt variant (if applicable): Feature enhancement request
- Next experiment (smallest change to try): Add more sophisticated natural language processing for task operations