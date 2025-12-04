'use client';

import Link from 'next/link';
import ThemeSwitcher from '@/components/ui/ThemeSwitcher';
import useAuthStore from '@/store/useAuthStore';
import { Button } from '@/components/ui/button';

const Header = () => {
  const { user, logout } = useAuthStore();

  return (
    <header className="bg-background border-b">
      <div className="container mx-auto flex justify-between items-center p-4">
        <Link href="/">
          <h1 className="text-2xl font-bold">4xbet</h1>
        </Link>
        <nav className="hidden md:flex gap-4">
          <Link href="/matches">Матчи</Link>
          <Link href="/my-bets">Ставки</Link>
          <Link href="/wallet">Кошелёк</Link>
        </nav>
        <div className="flex items-center gap-4">
          <ThemeSwitcher />
          {user ? (
            <>
              <Link href="/profile">
                <Button variant="ghost">Я</Button>
              </Link>
              <Button onClick={logout}>Выйти</Button>
            </>
          ) : (
            <>
              <Link href="/login">
                <Button variant="ghost">Войти</Button>
              </Link>
              <Link href="/register">
                <Button>Регистрация</Button>
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
