'use client';

import { useEffect } from 'react';

export default function HomePage() {
  useEffect(() => {
    // Direct redirect to login page on initial load
    window.location.href = '/login';
  }, []);

  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="text-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
        <p className="mt-4 text-gray-600">Redirecting to login...</p>
      </div>
    </div>
  );
}