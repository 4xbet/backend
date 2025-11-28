"use client";
import { useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';
import useAuthStore from '@/entities/user/model/store';
import { motion } from 'framer-motion';

interface AdminGuardProps {
  children: ReactNode;
}

const AdminGuard = ({ children }: AdminGuardProps) => {
  const router = useRouter();
  const { user, isLoggedIn, isLoading } = useAuthStore();

  useEffect(() => {
    if (!isLoading) {
      if (!isLoggedIn || user?.role !== 'admin') {
        router.replace('/');
      }
    }
  }, [isLoading, isLoggedIn, user, router]);

  if (isLoading || !isLoggedIn || user?.role !== 'admin') {
    return (
      <div className="flex items-center justify-center h-screen">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ repeat: Infinity, duration: 1, ease: 'linear' }}
          className="w-16 h-16 border-4 border-t-transparent border-blue-500 rounded-full"
        />
      </div>
    );
  }

  return <>{children}</>;
};

export default AdminGuard;
