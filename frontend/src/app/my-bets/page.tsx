"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import apiClient from "@/libraries/apiClient";
import { Bet, Match, Team } from "@/types";

export default function MyBetsPage() {
  const [bets, setBets] = useState<Bet[]>([]);
  const [matches, setMatches] = useState<Match[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [betsRes, matchesRes, teamsRes] = await Promise.all([
          apiClient.bets.getMyBets(),
          apiClient.matches.getAll(),
          apiClient.teams.getAll(),
        ]);
        setBets(betsRes.data);
        setMatches(matchesRes.data);
        setTeams(teamsRes.data);
      } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const getMatchDescription = (matchId: number) => {
    const match = matches.find((m) => m.id === matchId);
    if (!match) return "Н/Д";
    const team1 = teams.find((t) => t.id === match.home_team_id)?.name || "Н/Д";
    const team2 = teams.find((t) => t.id === match.away_team_id)?.name || "Н/Д";
    return `${team1} против ${team2}`;
  };

  const getOutcomeName = (outcome: string) => {
    switch (outcome) {
      case "win_home":
        return "Победа домашней команды";
      case "win_away":
        return "Победа гостевой команды";
      case "draw":
        return "Ничья";
      default:
        return outcome;
    }
  };

  const getStatusBadge = (status: string) => {
    const statusMap: Record<string, { text: string; className: string }> = {
      pending: { text: "Ожидание", className: "bg-yellow-100 text-yellow-800" },
      won: { text: "Выиграна", className: "bg-green-100 text-green-800" },
      lost: { text: "Проиграна", className: "bg-red-100 text-red-800" },
      cancelled: { text: "Отменена", className: "bg-gray-100 text-gray-800" },
    };

    const statusInfo = statusMap[status] || { text: status, className: "bg-gray-100 text-gray-800" };

    return (
      <span className={`px-2 py-1 rounded text-xs ${statusInfo.className}`}>
        {statusInfo.text}
      </span>
    );
  };

  if (loading) {
    return <div className="text-center py-10">Загрузка ваших ставок...</div>;
  }

  return (
    <div className="container mx-auto py-10">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <Card>
          <CardHeader>
            <CardTitle>Мои ставки</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Матч</TableHead>
                  <TableHead>Ваша ставка</TableHead>
                  <TableHead>Сумма ставки</TableHead>
                  <TableHead>Коэффициент</TableHead>
                  <TableHead>Потенциальный выигрыш</TableHead>
                  <TableHead>Статус</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {bets.length > 0 ? (
                  bets.map((bet) => {
                    const potentialWin = bet.amount_staked * (bet.odds_on_bet || 1);
                    return (
                      <TableRow key={bet.id}>
                        <TableCell>{getMatchDescription(bet.match_id)}</TableCell>
                        <TableCell>{getOutcomeName(bet.outcome)}</TableCell>
                        <TableCell>{bet.amount_staked.toFixed(2)} ₽</TableCell>
                        <TableCell>{bet.odds_on_bet?.toFixed(2) || "Н/Д"}</TableCell>
                        <TableCell>{potentialWin.toFixed(2)} ₽</TableCell>
                        <TableCell>{getStatusBadge(bet.status)}</TableCell>
                      </TableRow>
                    );
                  })
                ) : (
                  <TableRow>
                    <TableCell colSpan={6} className="text-center">
                      Вы еще не сделали ни одной ставки.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}