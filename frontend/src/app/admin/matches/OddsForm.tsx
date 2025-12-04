"use client";
import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import apiClient from "@/libraries/apiClient";
import toast from "react-hot-toast";
import { Match } from "@/types";

interface OddsFormProps {
  match: Match;
  onSuccess: () => void;
}

export default function OddsForm({ match, onSuccess }: OddsFormProps) {
  const [winHome, setWinHome] = useState("1.0");
  const [draw, setDraw] = useState("2.0");
  const [winAway, setWinAway] = useState("1.0");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.matches.updateOdds(match.id.toString(), {
        win_home: parseFloat(winHome),
        draw: parseFloat(draw),
        win_away: parseFloat(winAway),
      });
      toast.success("Коэффициенты успешно обновлены!");
      onSuccess();
    } catch (error: any) {
      console.error("Ошибка обновления коэффициентов:", error);
      toast.error("Не удалось обновить коэффициенты: " + (error.response?.data?.detail || error.message));
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label htmlFor="win-home">Победа домашней команды</Label>
        <Input
          id="win-home"
          type="number"
          value={winHome}
          onChange={(e) => setWinHome(e.target.value)}
          step="0.01"
          min="1.0"
          required
        />
      </div>
      <div>
        <Label htmlFor="draw">Ничья</Label>
        <Input
          id="draw"
          type="number"
          value={draw}
          onChange={(e) => setDraw(e.target.value)}
          step="0.01"
          min="1.0"
          required
        />
      </div>
      <div>
        <Label htmlFor="win-away">Победа гостевой команды</Label>
        <Input
          id="win-away"
          type="number"
          value={winAway}
          onChange={(e) => setWinAway(e.target.value)}
          step="0.01"
          min="1.0"
          required
        />
      </div>
      <Button type="submit">Обновить коэффициенты</Button>
    </form>
  );
}