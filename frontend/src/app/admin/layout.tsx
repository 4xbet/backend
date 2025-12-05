"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(true);
  const [isAdmin, setIsAdmin] = useState(false);
  const [userEmail, setUserEmail] = useState('');

  useEffect(() => {
    console.log('AdminLayout проверка авторизации...');
    
    const token = localStorage.getItem('authToken');
    
    if (!token) {
      console.log('Токен отсутствует, перенаправление на /matches');
      router.replace('/matches');
      return;
    }

    try {
      const payload = JSON.parse(atob(token.split('.')[1]));
      console.log('Декодированный токен:', payload);
      
      if (payload.role === 'admin') {
        setIsAdmin(true);
        setUserEmail(payload.sub);
        setIsLoading(false);
      } else {
        console.log('Не администратор, перенаправление. Роль:', payload.role);
        router.replace('/matches');
      }
    } catch (error) {
      console.error('Ошибка декодирования токена:', error);
      router.replace('/matches');
    }
  }, [router]);

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4">Проверка прав администратора...</p>
        </div>
      </div>
    );
  }

  if (!isAdmin) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 text-xl">Доступ запрещен</p>
          <p className="mt-2">У вас нет прав администратора</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-gray-800 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <h1 className="text-2xl font-bold">Панель администратора</h1>
          <div className="text-sm">
            <p>Добро пожаловать, <span className="font-semibold">{userEmail}</span></p>
            <p className="text-green-400">Роль: Администратор</p>
          </div>
        </div>
      </nav>
      <main className="container mx-auto p-4">
        {children}
      </main>
    </div>
  );
}