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
} from "@/components/ui/dialog";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import apiClient from "@/libraries/apiClient";
import { Team } from "@/types";
import TeamForm from "./TeamForm";
import toast from "react-hot-toast";

export default function AdminTeamsPage() {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [isDialogOpen, setDialogOpen] = useState(false);
  const [editingTeam, setEditingTeam] = useState<Team | undefined>(undefined);

  const fetchTeams = async () => {
    try {
      const response = await apiClient.teams.getAll();
      setTeams(response.data);
    } catch (error) {
      console.error("Ошибка при загрузке команд:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTeams();
  }, []);

  const handleDelete = async (id: number) => {
    if (confirm("Вы уверены, что хотите удалить эту команду?")) {
      try {
        await apiClient.teams.delete(id.toString());
        toast.success("Команда успешно удалена!");
        fetchTeams();
      } catch (error) {
        toast.error("Не удалось удалить команду.");
      }
    }
  };

  const handleSuccess = () => {
    setDialogOpen(false);
    setEditingTeam(undefined);
    fetchTeams();
  };

  if (loading) {
    return <div className="text-center py-10">Загрузка команд...</div>;
  }

  return (
    <div className="container mx-auto py-10">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Управление командами</CardTitle>
            <Dialog open={isDialogOpen} onOpenChange={setDialogOpen}>
              <DialogTrigger asChild>
                <Button onClick={() => setEditingTeam(undefined)}>Добавить команду</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>{editingTeam ? "Редактировать команду" : "Добавить новую команду"}</DialogTitle>
                </DialogHeader>
                <TeamForm team={editingTeam} onSuccess={handleSuccess} />
              </DialogContent>
            </Dialog>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>ID</TableHead>
                  <TableHead>Название</TableHead>
                  <TableHead>Действия</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {teams.map((team) => (
                  <TableRow key={team.id}>
                    <TableCell>{team.id}</TableCell>
                    <TableCell>{team.name}</TableCell>
                    <TableCell className="space-x-2">
                      <Button
                        variant="outline"
                        size="sm"
                        onClick={() => {
                          setEditingTeam(team);
                          setDialogOpen(true);
                        }}
                      >
                        Редактировать
                      </Button>
                      <Button
                        variant="destructive"
                        size="sm"
                        onClick={() => handleDelete(team.id)}
                      >
                        Удалить
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}