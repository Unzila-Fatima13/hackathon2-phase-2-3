import React, { useState, useEffect } from 'react';
import TaskItem from './TaskItem';
import { apiClient } from '../lib/api';

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

interface TaskListProps {
  userId?: string;
}

const TaskList: React.FC<TaskListProps> = ({ userId }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTasks();
  }, []);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null); // Reset error state
      const tasksData = await apiClient.getTasks();
      setTasks(tasksData);
    } catch (err) {
      console.error('Error loading tasks:', err);
      setError(err instanceof Error ? err.message : 'Failed to load tasks');
      // Still set loading to false even on error
      setLoading(false);
    } finally {
      // Ensure loading is always set to false in the end
      if (loading) {
        setLoading(false);
      }
    }
  };

  const handleToggleComplete = async (taskId: string, currentStatus: boolean) => {
    try {
      await apiClient.updateTask(taskId, { is_completed: !currentStatus });
      // Update the task in the local state
      setTasks(tasks.map(task =>
        task.id === taskId ? { ...task, is_completed: !currentStatus } : task
      ));
    } catch (err) {
      console.error('Error updating task:', err);
      alert('Failed to update task: ' + (err instanceof Error ? err.message : 'Unknown error'));
    }
  };

  const handleDelete = async (taskId: string) => {
    try {
      await apiClient.deleteTask(taskId);
      // Remove the task from the local state
      setTasks(tasks.filter(task => task.id !== taskId));
    } catch (err) {
      console.error('Error deleting task:', err);
      alert('Failed to delete task: ' + (err instanceof Error ? err.message : 'Unknown error'));
    }
  };

  if (loading) {
    return <div className="text-center py-4">Loading tasks...</div>;
  }

  if (error) {
    return (
      <div className="text-center py-4 text-red-500">
        <p>Error: {error}</p>
        <button
          onClick={loadTasks}
          className="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <h2 className="text-xl font-semibold">Your Tasks</h2>
      {tasks.length === 0 ? (
        <div className="text-center py-8 text-gray-500">
          No tasks yet. Create your first task!
        </div>
      ) : (
        <ul className="space-y-2">
          {tasks.map((task) => (
            <TaskItem
              key={task.id}
              task={task}
              onToggleComplete={handleToggleComplete}
              onDelete={handleDelete}
            />
          ))}
        </ul>
      )}
    </div>
  );
};

export default TaskList;