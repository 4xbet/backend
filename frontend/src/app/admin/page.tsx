"use client";
import { useEffect } from "react";
import Link from "next/link";

export default function AdminDashboardPage() {
  useEffect(() => {
    console.log('Страница администратора загружена');
    const token = localStorage.getItem('authToken');
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        console.log('Текущий пользователь:', payload.sub, 'Роль:', payload.role);
      } catch (e) {
        console.error('Ошибка декодирования:', e);
      }
    }
  }, []);

  return (
    <div className="py-8">
      <h1 className="text-3xl font-bold mb-6">Панель администратора</h1>
      
      <div className="mb-8 p-6 bg-white rounded-lg shadow">
        <h2 className="text-xl font-semibold mb-4">Быстрые действия</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Link
            href="/admin/teams"
            className="block p-4 bg-blue-50 hover:bg-blue-100 rounded-lg border border-blue-200 transition-colors"
          >
            <div className="flex items-center">
              <div className="w-10 h-10 bg-blue-100 rounded-lg flex items-center justify-center mr-3">
                <span className="text-xl">🏆</span>
              </div>
              <div>
                <h3 className="font-semibold">Управление командами</h3>
                <p className="text-sm text-gray-600">Добавление, редактирование или удаление команд</p>
              </div>
            </div>
          </Link>
          
          <Link
            href="/admin/matches"
            className="block p-4 bg-green-50 hover:bg-green-100 rounded-lg border border-green-200 transition-colors"
          >
            <div className="flex items-center">
              <div className="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center mr-3">
                <span className="text-xl">⚽</span>
              </div>
              <div>
                <h3 className="font-semibold">Управление матчами</h3>
                <p className="text-sm text-gray-600">Планирование матчей и установка коэффициентов</p>
              </div>
            </div>
          </Link>
        </div>
      </div>
      
      <div className="p-6 bg-gray-50 rounded-lg">
        <h2 className="text-xl font-semibold mb-4">Статус системы</h2>
        <div className="space-y-2">
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <span>Аутентификация: Работает</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <span>API Gateway: Подключен</span>
          </div>
          <div className="flex items-center">
            <div className="w-3 h-3 bg-green-500 rounded-full mr-2"></div>
            <span>Доступ администратора: Предоставлен</span>
          </div>
        </div>
      </div>
    </div>
  );
}