'use client';

import React, { useState, useEffect } from 'react';
import TaskList from '../../components/TaskList';
import TaskForm from '../../components/TaskForm';
import TaskChatbot from '../../components/TaskChatbot';
import { authService } from '../../lib/auth';

const DashboardPage: React.FC = () => {
  const [showForm, setShowForm] = useState(false);
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [isLoading, setIsLoading] = useState(true);
  const [hasAuth, setHasAuth] = useState(false);

  // Check authentication on mount
  useEffect(() => {
    const checkAuth = async () => {
      await authService.initialize(); // Wait for auth to initialize
      const isAuthenticated = authService.isAuthenticated();
      setHasAuth(isAuthenticated);
      setIsLoading(false);

      if (!isAuthenticated) {
        // Redirect to login if not authenticated
        window.location.href = '/login';
      }
    };

    checkAuth();
  }, []);

  const handleTaskCreated = () => {
    setShowForm(false);
    // Trigger a refresh of the task list
    setRefreshTrigger(prev => prev + 1);
  };

  const handleLogout = async () => {
    try {
      await authService.logout();
      window.location.href = '/login';
    } catch (error) {
      console.error('Logout error:', error);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (!hasAuth) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-600">Redirecting to login...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8 flex justify-between items-center">
          <h1 className="text-3xl font-bold text-gray-900">Todo Dashboard</h1>
          <button
            onClick={handleLogout}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
          >
            Logout
          </button>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-6 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2">
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-semibold text-gray-800">Your Tasks</h2>
              <button
                onClick={() => setShowForm(!showForm)}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                {showForm ? 'Cancel' : '+ Add Task'}
              </button>
            </div>

            {showForm && <TaskForm onTaskCreated={handleTaskCreated} />}

            <TaskList key={refreshTrigger} />
          </div>

          <div className="lg:col-span-1">
            <TaskChatbot onTaskUpdate={() => setRefreshTrigger(prev => prev + 1)} />
          </div>
        </div>
      </main>
    </div>
  );
};

export default DashboardPage;