"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import apiClient from "@/libraries/apiClient";
import { User } from "@/types";

export default function ProfilePage() {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchUser = async () => {
      try {
        const response = await apiClient.users.getMe();
        setUser(response.data);
      } catch (error) {
        console.error("Failed to fetch user:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchUser();
  }, []);

  if (loading) {
    return <div className="text-center py-10">Загрузка профиля...</div>;
  }

  if (!user) {
    return <div className="text-center py-10">Не удалось загрузить профиль пользователя.</div>;
  }

  return (
    <div className="container mx-auto py-10">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <Card>
          <CardHeader>
            <CardTitle>Мой профиль</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="font-semibold">Почта:</p>
              <p>{user.email}</p>
            </div>
            <div>
              <p className="font-semibold">Роль:</p>
              <p className="capitalize">{user.role}</p>
            </div>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
