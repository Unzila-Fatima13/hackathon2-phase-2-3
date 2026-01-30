'use client';

import React, { useState } from 'react';
import LoginForm from '../../components/LoginForm';
import Link from 'next/link';

const LoginPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);

  const handleSuccess = () => {
    setIsLoading(true);
    // Redirect to dashboard after successful login
    window.location.href = '/dashboard';
  };

  const handleError = (errorMessage: string) => {
    console.error('Login error:', errorMessage);
    setIsLoading(false);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gray-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
          <p className="mt-4 text-gray-600">Logging in...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Sign in to your account
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Or{' '}
          <Link href="/register" className="font-medium text-blue-600 hover:text-blue-500">
            create a new account
          </Link>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <LoginForm onSuccess={handleSuccess} onError={handleError} />
        </div>
      </div>
    </div>
  );
};

export default LoginPage;