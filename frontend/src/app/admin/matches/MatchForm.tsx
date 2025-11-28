"use client";
import { useState } from "react";
import { Button } from "@/shared/ui/button";
import { Input } from "@/shared/ui/input";
import { Label } from "@/shared/ui/label";
import apiClient from "@/shared/api";
import toast from "react-hot-toast";
import { Match, Team } from "@/shared/types";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/shared/ui/select";

interface MatchFormProps {
  match?: Match;
  teams: Team[];
  onSuccess: () => void;
}

export default function MatchForm({ match, teams, onSuccess }: MatchFormProps) {
  const [team1Id, setTeam1Id] = useState(match?.team1_id.toString() || "");
  const [team2Id, setTeam2Id] = useState(match?.team2_id.toString() || "");
  const [startTime, setStartTime] = useState(match?.start_time || "");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (team1Id === team2Id) {
      toast.error("Teams must be different.");
      return;
    }
    try {
      const matchData = {
        team1_id: parseInt(team1Id),
        team2_id: parseInt(team2Id),
        start_time: new Date(startTime).toISOString(),
      };
      // For now, there's no update functionality in the API for matches, only create
      await apiClient.matches.create(matchData);
      toast.success("Match created successfully!");
      onSuccess();
    } catch (error) {
      toast.error("Failed to save match.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label>Team 1</Label>
        <Select value={team1Id} onValueChange={setTeam1Id}>
          <SelectTrigger>
            <SelectValue placeholder="Select Team 1" />
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
        <Label>Team 2</Label>
        <Select value={team2Id} onValueChange={setTeam2Id}>
          <SelectTrigger>
            <SelectValue placeholder="Select Team 2" />
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
        <Label htmlFor="start-time">Start Time</Label>
        <Input
          id="start-time"
          type="datetime-local"
          value={startTime}
          onChange={(e) => setStartTime(e.target.value)}
          required
        />
      </div>
      <Button type="submit">Create Match</Button>
    </form>
  );
}
