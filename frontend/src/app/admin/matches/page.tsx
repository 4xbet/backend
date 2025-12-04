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
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
  DialogDescription, // ← Добавить этот импорт
} from "@/components/ui/dialog";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import apiClient from "@/libraries/apiClient";
import { Match, Team } from "@/types";
import MatchForm from "./MatchForm";
import OddsForm from "./OddsForm";

export default function AdminMatchesPage() {
  const [matches, setMatches] = useState<Match[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isMatchDialogOpen, setMatchDialogOpen] = useState(false);
  const [isOddsDialogOpen, setOddsDialogOpen] = useState(false);
  const [selectedMatch, setSelectedMatch] = useState<Match | undefined>(undefined);

  const fetchMatchesAndTeams = async () => {
    try {
      const [matchesRes, teamsRes] = await Promise.all([
        apiClient.matches.getAll(),
        apiClient.teams.getAll(),
      ]);
      setMatches(matchesRes.data);
      setTeams(teamsRes.data);
    } catch (error) {
      console.error("Ошибка при загрузке матчей или команд:", error);
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
                  <DialogDescription> {/* ← Теперь этот компонент доступен */}
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
                  <TableHead>Действия</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {matches.map((match) => (
                  <TableRow key={match.id}>
                    <TableCell>{match.id}</TableCell>
                    <TableCell>
                      {teams.find((t) => t.id === match.home_team_id)?.name || "Н/Д"} против{" "}
                      {teams.find((t) => t.id === match.away_team_id)?.name || "Н/Д"}
                    </TableCell>
                    <TableCell>
                      {new Date(match.start_time).toLocaleString()}
                    </TableCell>
                    <TableCell>
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setSelectedMatch(match);
                          setOddsDialogOpen(true);
                        }}
                      >
                        Редактировать коэффициенты
                      </Button>
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
            <DialogDescription> {}
              Установите коэффициенты для этого матча
            </DialogDescription>
          </DialogHeader>
          {selectedMatch && <OddsForm match={selectedMatch} onSuccess={handleSuccess} />}
        </DialogContent>
      </Dialog>
    </div>
  );
}