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
      return;
    }

    if (!isLoggedIn) {
      router.push('/login');
      return;
    }

    if (adminOnly && user?.role !== 'admin') {
      router.push('/matches');
    }
  }, [isLoggedIn, user, isLoading, adminOnly, router]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-gray-900"></div>
      </div>
    );
  }

  if (!isLoggedIn || (adminOnly && user?.role !== 'admin')) {
    return null; 
  }

  return <>{children}</>;
};

export default AuthGuard;
