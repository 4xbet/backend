"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import apiClient from "@/libraries/apiClient";
import toast from "react-hot-toast";
import { Match, Team, Wallet } from "@/types";

export default function MatchDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [match, setMatch] = useState<Match | null>(null);
  const [teams, setTeams] = useState<Team[]>([]);
  const [wallet, setWallet] = useState<Wallet | null>(null);
  const [amount, setAmount] = useState<string>("");
  const [teamId, setTeamId] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (id) {
      const fetchMatchData = async () => {
        try {
          const [matchRes, teamsRes, walletRes] = await Promise.all([
            apiClient.matches.getById(id),
            apiClient.teams.getAll(),
            apiClient.users.getWallet(),
          ]);
          setMatch(matchRes.data);
          setTeams(teamsRes.data);
          setWallet(walletRes.data);
        } catch (error) {
          console.error("Ошибка при загрузке деталей матча:", error);
        } finally {
          setLoading(false);
        }
      };
      fetchMatchData();
    }
  }, [id]);

  const getTeamName = (teamId: number) => {
    return teams.find((t) => t.id === teamId)?.name || `Команда ${teamId}`;
  };

  const handleBet = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!teamId || !amount) {
      toast.error("Пожалуйста, выберите команду и введите сумму.");
      return;
    }
    const betAmount = parseFloat(amount);
    if (wallet && wallet.balance < betAmount) {
      toast.error("Недостаточно средств.");
      return;
    }
    
    // Определяем outcome на основе выбранной команды
    let outcome = "";
    if (match && teamId === match.home_team_id) {
      outcome = "win_home";
    } else if (match && teamId === match.away_team_id) {
      outcome = "win_away";
    } else {
      toast.error("Не удалось определить тип ставки");
      return;
    }
    
    try {
      // Отправляем данные с правильными полями для bets_service
      await apiClient.bets.create({
        match_id: parseInt(id),
        outcome: outcome,           // ← Изменено: team_id → outcome
        amount_staked: betAmount,   // ← Изменено: amount → amount_staked
      });
      toast.success("Ставка успешно размещена!");
      const walletRes = await apiClient.users.getWallet();
      setWallet(walletRes.data);
      setAmount(""); // Очистить поле ввода
      setTeamId(null); // Сбросить выбор команды
    } catch (error: any) {
      console.error("Полная ошибка ставки:", error);
      console.error("Ответ сервера:", error.response?.data);
      toast.error("Не удалось разместить ставку: " + (error.response?.data?.detail || error.message));
    }
  };

  if (loading) {
    return <div className="text-center py-10">Загрузка деталей матча...</div>;
  }

  if (!match) {
    return <div className="text-center py-10">Матч не найден.</div>;
  }

  return (
    <div className="container mx-auto py-10">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <Card>
          <CardHeader>
            <CardTitle>
              Матч: {getTeamName(match.home_team_id)} против {getTeamName(match.away_team_id)}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p>
              <strong>Время начала:</strong>{" "}
              {new Date(match.start_time).toLocaleString()}
            </p>
            <div className="my-4">
              <p>
                <strong>Ваш баланс:</strong> {wallet?.balance.toFixed(2)}
              </p>
            </div>
            <form onSubmit={handleBet} className="space-y-4">
              <div>
                <Label>Выберите команду</Label>
                <div className="flex gap-4">
                  <Button
                    type="button"
                    variant={teamId === match.home_team_id ? "default" : "outline"}
                    onClick={() => setTeamId(match.home_team_id)}
                  >
                    {getTeamName(match.home_team_id)} (Победа домашней)
                  </Button>
                  <Button
                    type="button"
                    variant={teamId === match.away_team_id ? "default" : "outline"}
                    onClick={() => setTeamId(match.away_team_id)}
                  >
                    {getTeamName(match.away_team_id)} (Победа гостевой)
                  </Button>
                </div>
              </div>
              <div>
                <Label htmlFor="amount">Сумма ставки</Label>
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
              <Button type="submit">Сделать ставку</Button>
            </form>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}