'use client';
import Link from 'next/link';
import { motion } from 'framer-motion';
import useAuthStore from '@/entities/user/model/store';
import { Button } from '@/shared/ui/button';
import { LogOut, User, Shield, BarChart2, Ticket } from 'lucide-react';
import toast from 'react-hot-toast';

const Header = () => {
  const { isLoggedIn, user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    toast.success('Вы успешно вышли из системы');
  };

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.5 }}
      className="sticky top-0 z-50 w-full border-b border-border/40 bg-background/95 backdrop-blur"
    >
      <div className="container flex h-16 items-center justify-between">
        <Link href="/" className="flex items-center space-x-2">
          <motion.div whileHover={{ rotate: 360, scale: 1.1 }}>
            <BarChart2 className="h-8 w-8 text-primary" />
          </motion.div>
          <span className="font-bold text-lg">4xBet</span>
        </Link>
        <nav className="hidden md:flex items-center space-x-6">
          <Link href="/matches" className="text-sm font-medium transition-colors hover:text-primary">
            Матчи
          </Link>
          {isLoggedIn && (
            <>
              <Link href="/my-bets" className="text-sm font-medium transition-colors hover:text-primary">
                Мои ставки
              </Link>
              <Link href="/wallet" className="text-sm font-medium transition-colors hover:text-primary">
                Кошелек
              </Link>
            </>
          )}
        </nav>
        <div className="flex items-center space-x-4">
          {isLoggedIn ? (
            <>
              {user?.role === 'admin' && (
                <Link href="/admin" passHref>
                  <Button variant="outline" size="sm">
                    <Shield className="mr-2 h-4 w-4" />
                    Админ
                  </Button>
                </Link>
              )}
              <Link href="/profile" passHref>
                <Button variant="ghost" size="sm">
                  <User className="mr-2 h-4 w-4" />
                  Профиль
                </Button>
              </Link>
              <Button onClick={handleLogout} variant="destructive" size="sm">
                <LogOut className="mr-2 h-4 w-4" />
                Выйти
              </Button>
            </>
          ) : (
            <>
              <Link href="/login" passHref>
                <Button variant="outline" size="sm">
                  Войти
                </Button>
              </Link>
              <Link href="/register" passHref>
                <Button size="sm">Регистрация</Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </motion.header>
  );
};

export default Header;
