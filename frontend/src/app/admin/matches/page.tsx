'use client';
import { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription,
} from '@/components/ui/dialog';
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from '@/components/ui/alert-dialog';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import apiClient from '@/libraries/apiClient';
import { toast } from 'sonner';
import { Match, Team } from '@/types';
import MatchForm from './MatchForm';
import OddsForm from './OddsForm';

export default function AdminMatchesPage() {
  const [matches, setMatches] = useState<Match[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isMatchDialogOpen, setMatchDialogOpen] = useState(false);
  const [isOddsDialogOpen, setOddsDialogOpen] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState<Match | undefined>(undefined);
  const [isConfirmDialogOpen, setConfirmDialogOpen] = useState(false);

  const fetchMatchesAndTeams = async () => {
    try {
      const [matchesRes, teamsRes] = await Promise.all([apiClient.matches.getAll(), apiClient.teams.getAll()]);
      setMatches(matchesRes.data);
      setTeams(teamsRes.data);
    } catch (error) {
      console.error('Ошибка при загрузке матчей или команд:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMatchesAndTeams();
  }, []);

  const handleSuccess = () => {
    setMatchDialogOpen(false);
    setOddsDialogOpen(false);
    setSelectedMatch(undefined);
    fetchMatchesAndTeams();
  };

  const handleCompleteMatch = async (matchId: number) => {
    try {
      await apiClient.admin.completeMatch(matchId);
      toast.success('Матч успешно завершен!');
      fetchMatchesAndTeams();
    } catch (error) {
      console.error('Ошибка при завершении матча:', error);
      toast.error('Не удалось завершить матч.');
    } finally {
      setConfirmDialogOpen(false);
      setSelectedMatch(undefined);
    }
  };

  const handleStartMatch = async (matchId: number) => {
    try {
      await apiClient.admin.startMatch(matchId);
      toast.success('Матч успешно начат!');
      fetchMatchesAndTeams();
    } catch (error) {
      console.error('Ошибка при начале матча:', error);
      toast.error('Не удалось начать матч.');
    }
  };

  if (loading) {
    return <div className="text-center py-10">Загрузка матчей...</div>;
  }

  return (
    <div className="container mx-auto py-10">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Управление матчами</CardTitle>
            <Dialog open={isMatchDialogOpen} onOpenChange={setMatchDialogOpen}>
              <DialogTrigger asChild>
                <Button>Добавить матч</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Добавить новый матч</DialogTitle>
                  <DialogDescription>
                    {' '}
                    {}
                    Заполните форму для создания нового матча
                  </DialogDescription>
                </DialogHeader>
                <MatchForm teams={teams} onSuccess={handleSuccess} />
              </DialogContent>
            </Dialog>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Команды</TableHead>
                  <TableHead>Время начала</TableHead>
                  <TableHead>Статус</TableHead>
                  <TableHead>Действия</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {matches.map((match) => (
                  <TableRow key={match.id}>
                    <TableCell>{match.id}</TableCell>
                    <TableCell>
                      {teams.find((t) => t.id === match.home_team_id)?.name || 'Н/Д'} против{' '}
                      {teams.find((t) => t.id === match.away_team_id)?.name || 'Н/Д'}
                    </TableCell>
                    <TableCell>{new Date(match.start_time).toLocaleString()}</TableCell>
                    <TableCell>{match.status}</TableCell>
                    <TableCell className="space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setSelectedMatch(match);
                          setOddsDialogOpen(true);
                        }}
                      >
                        Коэфф.
                      </Button>
                      {match.status === 'scheduled' && (
                        <Button variant="default" size="sm" onClick={() => handleStartMatch(match.id)}>
                          Начать
                        </Button>
                      )}
                      {match.status === 'active' && (
                        <AlertDialog>
                          <AlertDialogTrigger asChild>
                            <Button variant="destructive" size="sm" onClick={() => setSelectedMatch(match)}>
                              Завершить
                            </Button>
                          </AlertDialogTrigger>
                          <AlertDialogContent>
                            <AlertDialogHeader>
                              <AlertDialogTitle>Завершить матч принудительно?</AlertDialogTitle>
                              <AlertDialogDescription>
                                Это действие нельзя отменить. Победитель будет выбран случайным образом, а выигрыши
                                распределены между игроками, сделавшими ставки на него.
                              </AlertDialogDescription>
                            </AlertDialogHeader>
                            <AlertDialogFooter>
                              <AlertDialogCancel>Отмена</AlertDialogCancel>
                              <AlertDialogAction onClick={() => selectedMatch && handleCompleteMatch(selectedMatch.id)}>
                                Подтвердить
                              </AlertDialogAction>
                            </AlertDialogFooter>
                          </AlertDialogContent>
                        </AlertDialog>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </motion.div>
      <Dialog open={isOddsDialogOpen} onOpenChange={setOddsDialogOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Редактировать коэффициенты</DialogTitle>
            <DialogDescription>
              {' '}
              {}
              Установите коэффициенты для этого матча
            </DialogDescription>
          </DialogHeader>
          {selectedMatch && <OddsForm match={selectedMatch} onSuccess={handleSuccess} />}
        </DialogContent>
      </Dialog>
    </div>
  );
}
