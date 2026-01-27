import React from 'react';

interface Task {
  id: string;
  title: string;
  description?: string;
  is_completed: boolean;
  created_at: string;
  updated_at: string;
  due_date?: string;
  user_id: string;
}

interface TaskItemProps {
  task: Task;
  onToggleComplete: (taskId: string, currentStatus: boolean) => void;
  onDelete: (taskId: string) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onToggleComplete, onDelete }) => {
  const handleToggleComplete = () => {
    onToggleComplete(task.id, task.is_completed);
  };

  const handleDelete = () => {
    onDelete(task.id);
  };

  return (
    <li className="border rounded-lg p-4 bg-white shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-start">
        <input
          type="checkbox"
          checked={task.is_completed}
          onChange={handleToggleComplete}
          className="mt-1 h-4 w-4 text-blue-600 rounded focus:ring-blue-500"
        />
        <div className="ml-3 flex-1 min-w-0">
          <p className={`text-sm font-medium ${task.is_completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {task.title}
          </p>
          {task.description && (
            <p className={`text-sm ${task.is_completed ? 'line-through text-gray-400' : 'text-gray-500'}`}>
              {task.description}
            </p>
          )}
          {task.due_date && (
            <p className="text-xs text-gray-400 mt-1">
              Due: {new Date(task.due_date).toLocaleDateString()}
            </p>
          )}
          <p className="text-xs text-gray-400 mt-1">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </p>
        </div>
        <button
          onClick={handleDelete}
          className="ml-2 text-red-500 hover:text-red-700 text-sm"
        >
          Delete
        </button>
      </div>
    </li>
  );
};

export default TaskItem;