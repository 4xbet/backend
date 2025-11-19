'use client';

import { useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import useAuthStore from '@/store/useAuthStore';

interface AuthGuardProps {
  children: ReactNode;
  adminOnly?: boolean;
}

const AuthGuard = ({ children, adminOnly = false }: AuthGuardProps) => {
  const { isLoggedIn, user, isLoading, initialize } = useAuthStore();
  const router = useRouter();

  useEffect(() => {
    initialize();
  }, [initialize]);

  useEffect(() => {
    if (isLoading) {
      return; // Wait for initialization to complete
    }

    if (!isLoggedIn) {
      router.push('/login');
      return;
    }

    if (adminOnly && user?.role !== 'admin') {
      router.push('/matches'); // Redirect non-admins from admin routes
    }
  }, [isLoggedIn, user, isLoading, adminOnly, router]);

  if (isLoading || !isLoggedIn || (adminOnly && user?.role !== 'admin')) {
    // You can replace this with a beautiful spinner component
    return (
      <div className="flex items-center justify-center min-h-screen">
        <p>Loading...</p>
      </div>
    );
  }

  return <>{children}</>;
};

export default AuthGuard;
