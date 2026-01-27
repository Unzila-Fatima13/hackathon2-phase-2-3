'use client';

import React, { useState, useRef, useEffect } from 'react';
import { apiClient } from '../lib/api';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'bot';
  timestamp: Date;
}

const TaskChatbot: React.FC<{ onTaskUpdate?: () => void }> = ({ onTaskUpdate }) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 1,
      text: "Hello! I'm your task management assistant. You can ask me to add, complete, or delete tasks using natural language.",
      sender: 'bot',
      timestamp: new Date(),
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Scroll to bottom of messages
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  // Parse natural language commands
  const parseCommand = (input: string): { action: string; params: any } => {
    const lowerInput = input.toLowerCase().trim();

    // Add task commands
    if (lowerInput.includes('add task') || lowerInput.includes('add ') || lowerInput.includes('create task') || lowerInput.includes('new task')) {
      let description = '';

      for (const prefix of ['add task ', 'add a task ', 'add ', 'create task ', 'new task ']) {
        if (lowerInput.startsWith(prefix)) {
          description = input.substring(prefix.length).trim();
          break;
        }
      }

      if (description) {
        return { action: 'add_task', params: { description } };
      }
    }

    // Complete/done task commands
    if (lowerInput.includes('complete task') || lowerInput.includes('complete ') || lowerInput.includes('done ') || lowerInput.includes('finish task')) {
      // First try to extract numbers (task IDs)
      const numbers = input.match(/\d+/g);
      if (numbers && numbers.length > 0) {
        return { action: 'complete_task', params: { taskId: parseInt(numbers[0]) } };
      }

      // If no numbers found, extract the task name after the command
      for (const prefix of ['complete task ', 'complete ', 'done ', 'finish task ']) {
        if (lowerInput.startsWith(prefix)) {
          const taskName = input.substring(prefix.length).trim();
          if (taskName) {
            return { action: 'complete_task', params: { taskId: taskName } };
          }
        }
      }

      return { action: 'error', params: { message: 'Please specify which task to complete by number or name.' } };
    }

    // Delete/remove task commands
    if (lowerInput.includes('delete task') || lowerInput.includes('delete ') || lowerInput.includes('remove task') || lowerInput.includes('remove ')) {
      // First try to extract numbers (task IDs)
      const numbers = input.match(/\d+/g);
      if (numbers && numbers.length > 0) {
        return { action: 'delete_task', params: { taskId: parseInt(numbers[0]) } };
      }

      // If no numbers found, extract the task name after the command
      for (const prefix of ['delete task ', 'delete ', 'remove task ', 'remove ']) {
        if (lowerInput.startsWith(prefix)) {
          const taskName = input.substring(prefix.length).trim();
          if (taskName) {
            return { action: 'delete_task', params: { taskId: taskName } };
          }
        }
      }

      return { action: 'error', params: { message: 'Please specify which task to delete by number or name.' } };
    }

    // List tasks commands
    if (lowerInput.includes('show tasks') || lowerInput.includes('view tasks') || lowerInput.includes('list tasks') || lowerInput.includes('my tasks') || lowerInput.includes('all tasks')) {
      return { action: 'list_tasks', params: {} };
    }

    // Help commands
    if (lowerInput.includes('help') || lowerInput.includes('what can you do') || lowerInput.includes('commands') || lowerInput.includes('what can i do')) {
      return { action: 'help', params: {} };
    }

    return { action: 'unknown', params: { message: "I didn't understand that command. Type 'help' to see what I can do." } };
  };

  // Actual API calls to backend
  const addTask = async (description: string) => {
    try {
      const response = await apiClient.createTask({
        title: description,
        description: description
      });
      if (onTaskUpdate) onTaskUpdate();
      return `Added task: "${description}"`;
    } catch (error) {
      console.error('Error adding task:', error);
      return `Failed to add task: ${(error as Error).message}`;
    }
  };

  // Helper function to get tasks by name
  const findTaskByName = async (partialName: string) => {
    try {
      const tasks = await apiClient.getTasks();
      if (tasks && Array.isArray(tasks)) {
        // Find task that contains the partial name (case insensitive)
        const foundTask = tasks.find((task: any) =>
          task.title.toLowerCase().includes(partialName.toLowerCase()) ||
          task.description?.toLowerCase().includes(partialName.toLowerCase())
        );
        return foundTask;
      }
      return null;
    } catch (error) {
      console.error('Error finding task by name:', error);
      return null;
    }
  };

  const completeTask = async (taskId: number | string) => {
    try {
      let actualTaskId: string;

      if (typeof taskId === 'number') {
        // If taskId is a number, use it directly
        actualTaskId = taskId.toString();
      } else {
        // If taskId is a string (like a task name), try to find it
        const foundTask = await findTaskByName(taskId);
        if (foundTask) {
          actualTaskId = foundTask.id.toString();
        } else {
          return `Could not find task containing "${taskId}". Please use task number or check spelling.`;
        }
      }

      const response = await apiClient.updateTask(actualTaskId, {
        is_completed: true
      });
      if (onTaskUpdate) onTaskUpdate();
      // Get the task title to show in the response
      const task = await apiClient.getTasks().then((tasks: any[]) =>
        tasks.find((t: any) => t.id.toString() === actualTaskId)
      );
      return `Marked task "${task?.title || actualTaskId}" as complete`;
    } catch (error) {
      console.error('Error completing task:', error);
      return `Failed to complete task: ${(error as Error).message}`;
    }
  };

  const deleteTask = async (taskId: number | string) => {
    try {
      let actualTaskId: string;

      if (typeof taskId === 'number') {
        // If taskId is a number, use it directly
        actualTaskId = taskId.toString();
      } else {
        // If taskId is a string (like a task name), try to find it
        const foundTask = await findTaskByName(taskId);
        if (foundTask) {
          actualTaskId = foundTask.id.toString();
        } else {
          return `Could not find task containing "${taskId}". Please use task number or check spelling.`;
        }
      }

      const response = await apiClient.deleteTask(actualTaskId);
      if (onTaskUpdate) onTaskUpdate();
      // Get the task title to show in the response
      const task = await apiClient.getTasks().then((tasks: any[]) =>
        tasks.find((t: any) => t.id.toString() === actualTaskId)
      );
      return `Deleted task "${task?.title || actualTaskId}"`;
    } catch (error) {
      console.error('Error deleting task:', error);
      return `Failed to delete task: ${(error as Error).message}`;
    }
  };

  const listTasks = async () => {
    try {
      const tasks = await apiClient.getTasks();
      if (tasks && Array.isArray(tasks) && tasks.length > 0) {
        let taskList = "Here are your tasks:\n";
        tasks.forEach((task: any, index: number) => {
          const status = task.is_completed ? "[Completed]" : "[Pending]";
          // Use the actual task ID from the database instead of index
          taskList += `${task.id}. ${status} ${task.title}\n`;
        });
        return taskList;
      } else {
        return "You have no tasks yet. Add some tasks!";
      }
    } catch (error) {
      console.error('Error listing tasks:', error);
      return `Failed to load tasks: ${(error as Error).message}`;
    }
  };

  // Process commands with actual API calls
  const processCommand = async (command: { action: string; params: any }): Promise<string> => {
    switch (command.action) {
      case 'add_task':
        return await addTask(command.params.description);
      case 'complete_task':
        return await completeTask(command.params.taskId);
      case 'delete_task':
        return await deleteTask(command.params.taskId);
      case 'list_tasks':
        return await listTasks();
      case 'help':
        return (
          "I can help you manage tasks!\n\n" +
          "Commands I understand:\n" +
          "- 'add task [description]' or 'add [description]' to add a task\n" +
          "- 'complete task [number]' or 'done [number]' to mark as complete\n" +
          "- 'complete task [name]' or 'done [name]' to mark by name\n" +
          "- 'delete task [number]' or 'remove [number]' to delete by number\n" +
          "- 'delete task [name]' or 'remove [name]' to delete by name\n" +
          "- 'show tasks' or 'list tasks' to view all tasks\n" +
          "- 'help' to show this message"
        );
      case 'error':
        return command.params.message;
      case 'unknown':
        return command.params.message;
      default:
        return "I'm not sure how to handle that. Type 'help' for assistance.";
    }
  };

  const handleSendMessage = async () => {
    if (!inputValue.trim() || isProcessing) return;

    // Add user message
    const userMessage: Message = {
      id: messages.length + 1,
      text: inputValue,
      sender: 'user',
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsProcessing(true);

    try {
      // Parse the command
      const command = parseCommand(inputValue);

      // Process command with actual API calls
      const response = await processCommand(command);

      // Add bot response
      const botMessage: Message = {
        id: messages.length + 2,
        text: response,
        sender: 'bot',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: messages.length + 2,
        text: "Sorry, I encountered an error processing your request.",
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <div className="border border-gray-200 rounded-lg shadow-sm bg-white">
      <div className="p-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Task Assistant</h3>
        <p className="text-sm text-gray-500">Chat with me to manage your tasks!</p>
      </div>

      <div className="h-64 overflow-y-auto p-4 bg-gray-50">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`mb-3 ${
              message.sender === 'user' ? 'text-right' : 'text-left'
            }`}
          >
            <div
              className={`inline-block p-3 rounded-lg max-w-xs lg:max-w-md ${
                message.sender === 'user'
                  ? 'bg-blue-500 text-white rounded-br-none'
                  : 'bg-gray-200 text-gray-800 rounded-bl-none'
              }`}
            >
              <div className="whitespace-pre-wrap">{message.text}</div>
              <div
                className={`text-xs mt-1 ${
                  message.sender === 'user' ? 'text-blue-100' : 'text-gray-500'
                }`}
              >
                {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
              </div>
            </div>
          </div>
        ))}
        {isProcessing && (
          <div className="mb-3 text-left">
            <div className="inline-block p-3 rounded-lg bg-gray-200 text-gray-800 rounded-bl-none">
              <div className="flex items-center">
                <div className="animate-pulse">Processing...</div>
              </div>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="p-4 border-t border-gray-200">
        <div className="flex">
          <input
            type="text"
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Type a command... (e.g., 'add task Buy groceries')"
            className="flex-1 border border-gray-300 rounded-l-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            disabled={isProcessing}
          />
          <button
            onClick={handleSendMessage}
            disabled={isProcessing || !inputValue.trim()}
            className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Send
          </button>
        </div>
        <div className="mt-2 text-xs text-gray-500">
          Examples: "add task Buy groceries", "show tasks", "done 1", "delete task 2"
        </div>
      </div>
    </div>
  );
};

export default TaskChatbot;