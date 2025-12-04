'use client';
import { useState } from 'react';
import { Button } from '@/shared/ui/button';
import { Input } from '@/shared/ui/input';
import { Label } from '@/shared/ui/label';
import apiClient from '@/shared/api';
import toast from 'react-hot-toast';
import { Match } from '@/shared/types';

interface OddsFormProps {
  match: Match;
  onSuccess: () => void;
}

export default function OddsForm({ match, onSuccess }: OddsFormProps) {
  const [oddsTeam1, setOddsTeam1] = useState('1.0');
  const [oddsTeam2, setOddsTeam2] = useState('1.0');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await apiClient.matches.updateOdds(match.id.toString(), {
        odds_team1: parseFloat(oddsTeam1),
        odds_team2: parseFloat(oddsTeam2),
      });
      toast.success('Odds updated successfully!');
      onSuccess();
    } catch (error) {
      toast.error('Failed to update odds.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label htmlFor="odds-team1">Odds Team 1</Label>
        <Input
          id="odds-team1"
          type="number"
          value={oddsTeam1}
          onChange={(e) => setOddsTeam1(e.target.value)}
          step="0.01"
          required
        />
      </div>
      <div>
        <Label htmlFor="odds-team2">Odds Team 2</Label>
        <Input
          id="odds-team2"
          type="number"
          value={oddsTeam2}
          onChange={(e) => setOddsTeam2(e.target.value)}
          step="0.01"
          required
        />
      </div>
      <Button type="submit">Update Odds</Button>
    </form>
  );
}
