import React from 'react';
import { authService } from '../lib/auth';
import { useRouter } from 'next/navigation';
import { useEffect, useState } from 'react';

interface ProtectedRouteProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = ({ children, fallback = null }) => {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null); // null indicates loading state

  useEffect(() => {
    const checkAuth = async () => {
      const auth = authService.isAuthenticated();
      setIsAuthenticated(auth);

      if (!auth) {
        router.push('/login'); // Redirect to login if not authenticated
      }
    };

    checkAuth();
  }, [router]);

  // Show fallback or nothing while checking authentication
  if (isAuthenticated === null) {
    return fallback || <div>Loading...</div>;
  }

  // If authenticated, show the protected content
  if (isAuthenticated) {
    return <>{children}</>;
  }

  // If not authenticated, show fallback (which should redirect via router)
  return <>{fallback}</>;
};

export default ProtectedRoute;