import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import apiClient from "@/libraries/apiClient";
import toast from "react-hot-toast";
import { Match, Team } from "@/types";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";

interface MatchFormProps {
  match?: Match;
  teams: Team[];
  onSuccess: () => void;
}

export default function MatchForm({ match, teams, onSuccess }: MatchFormProps) {
  const [homeTeamId, setHomeTeamId] = useState(match?.home_team_id?.toString() || "");
  const [awayTeamId, setAwayTeamId] = useState(match?.away_team_id?.toString() || "");
  const [startTime, setStartTime] = useState(match?.start_time || "");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (homeTeamId === awayTeamId) {
      toast.error("Команды должны быть разными.");
      return;
    }
    try {
      const matchData = {
        home_team_id: parseInt(homeTeamId),
        away_team_id: parseInt(awayTeamId),
        start_time: new Date(startTime).toISOString(),
      };
      console.log("Отправляемые данные:", matchData); // Для отладки
      await apiClient.matches.create(matchData);
      toast.success("Матч успешно создан!");
      onSuccess();
    } catch (error: any) {
      console.error("Ошибка при создании матча:", error);
      toast.error("Не удалось сохранить матч: " + (error.response?.data?.detail || error.message));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label>Домашняя команда</Label>
        <Select value={homeTeamId} onValueChange={setHomeTeamId}>
          <SelectTrigger>
            <SelectValue placeholder="Выберите домашнюю команду" />
          </SelectTrigger>
          <SelectContent>
            {teams.map((team) => (
              <SelectItem key={team.id} value={team.id.toString()}>
                {team.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div>
        <Label>Гостевая команда</Label>
        <Select value={awayTeamId} onValueChange={setAwayTeamId}>
          <SelectTrigger>
            <SelectValue placeholder="Выберите гостевую команду" />
          </SelectTrigger>
          <SelectContent>
            {teams.map((team) => (
              <SelectItem key={team.id} value={team.id.toString()}>
                {team.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div>
        <Label htmlFor="start-time">Время начала</Label>
        <Input
          id="start-time"
          type="datetime-local"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          required
        />
      </div>
      <Button type="submit">Создать матч</Button>
    </form>
  );
}