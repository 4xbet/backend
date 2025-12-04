'use client';
import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/shared/ui/table';
import { Card, CardContent, CardHeader, CardTitle } from '@/shared/ui/card';
import apiClient from '@/shared/api';
import { Bet, Match, Team } from '@/shared/types';

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
        console.error('Failed to fetch data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const getMatchDescription = (matchId: number) => {
    const match = matches.find((m) => m.id === matchId);
    if (!match) return 'N/A';
    const team1 = teams.find((t) => t.id === match.team1_id)?.name || 'N/A';
    const team2 = teams.find((t) => t.id === match.team2_id)?.name || 'N/A';
    return `${team1} vs ${team2}`;
  };

  const getTeamName = (teamId: number) => {
    return teams.find((t) => t.id === teamId)?.name || 'N/A';
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
                  <TableHead>Сумма</TableHead>
                  <TableHead>Статус</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {bets.length > 0 ? (
                  bets.map((bet) => (
                    <TableRow key={bet.id}>
                      <TableCell>{getMatchDescription(bet.match_id)}</TableCell>
                      <TableCell>{getTeamName(bet.team_id)}</TableCell>
                      <TableCell>{bet.amount.toFixed(2)}</TableCell>
                      <TableCell className="capitalize">{bet.status}</TableCell>
                    </TableRow>
                  ))
                ) : (
                  <TableRow>
                    <TableCell colSpan={4} className="text-center">
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
