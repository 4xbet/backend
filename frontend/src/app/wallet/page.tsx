"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Button } from "@/shared/ui/button";
import { Input } from "@/shared/ui/input";
import { Label } from "@/shared/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/card";
import apiClient from "@/shared/api";
import toast from "react-hot-toast";
import { Wallet } from "@/shared/types";

export default function WalletPage() {
  const [wallet, setWallet] = useState<Wallet | null>(null);
  const [amount, setAmount] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(true);

  const fetchWallet = async () => {
    try {
      const response = await apiClient.users.getWallet();
      setWallet(response.data);
    } catch (error) {
      console.error("Failed to fetch wallet:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchWallet();
  }, []);

  const handleTopUp = async (e: React.FormEvent) => {
    e.preventDefault();
    const topUpAmount = parseFloat(amount);
    if (isNaN(topUpAmount) || topUpAmount <= 0) {
      toast.error("Пожалуйста, введите действительную сумму.");
      return;
    }
    try {
      await apiClient.users.updateWallet({ amount: topUpAmount });
      toast.success("Кошелек успешно пополнен!");
      fetchWallet(); // Refresh wallet balance
      setAmount("");
    } catch (error) {
      toast.error("Не удалось пополнить кошелек.");
    }
  };

  if (loading) {
    return <div className="text-center py-10">Загрузка кошелька...</div>;
  }

  return (
    <div className="container mx-auto py-10">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <Card>
          <CardHeader>
            <CardTitle>Мой кошелек</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="mb-6">
              <p className="text-lg font-semibold">Текущий баланс:</p>
              <p className="text-3xl">
                {wallet ? wallet.balance.toFixed(2) : "0.00"}
              </p>
            </div>
            <form onSubmit={handleTopUp} className="space-y-4">
              <h2 className="text-xl font-semibold">Пополнить</h2>
              <div>
                <Label htmlFor="amount">Сумма</Label>
                <Input
                  id="amount"
                  type="number"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  min="0.01"
                  step="0.01"
                  required
                />
              </div>
              <Button type="submit">Добавить средства</Button>
            </form>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
