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
import { Match, Wallet } from "@/types";

export default function MatchDetailPage() {
  const params = useParams();
  const id = params.id as string;
  const [match, setMatch] = useState<Match | null>(null);
  const [wallet, setWallet] = useState<Wallet | null>(null);
  const [amount, setAmount] = useState<string>("");
  const [teamId, setTeamId] = useState<number | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    if (id) {
      const fetchMatchAndWallet = async () => {
        try {
          const [matchRes, walletRes] = await Promise.all([
            apiClient.matches.getById(id),
            apiClient.users.getWallet(),
          ]);
          setMatch(matchRes.data);
          setWallet(walletRes.data);
        } catch (error) {
          console.error("Failed to fetch match details:", error);
        } finally {
          setLoading(false);
        }
      };
      fetchMatchAndWallet();
    }
  }, [id]);

  const handleBet = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!teamId || !amount) {
      toast.error("Please select a team and enter an amount.");
      return;
    }
    const betAmount = parseFloat(amount);
    if (wallet && wallet.balance < betAmount) {
      toast.error("Insufficient balance.");
      return;
    }
    try {
      await apiClient.bets.create({
        match_id: parseInt(id),
        team_id: teamId,
        amount: betAmount,
      });
      toast.success("Bet placed successfully!");
      // Refresh wallet balance
      const walletRes = await apiClient.users.getWallet();
      setWallet(walletRes.data);
    } catch (error) {
      toast.error("Failed to place bet.");
    }
  };

  if (loading) {
    return <div className="text-center py-10">Loading match details...</div>;
  }

  if (!match) {
    return <div className="text-center py-10">Match not found.</div>;
  }

  return (
    <div className="container mx-auto py-10">
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
        <Card>
          <CardHeader>
            <CardTitle>
              Match: Team {match.team1_id} vs Team {match.team2_id}
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p>
              <strong>Start Time:</strong>{" "}
              {new Date(match.start_time).toLocaleString()}
            </p>
            <div className="my-4">
              <p>
                <strong>Your Balance:</strong> {wallet?.balance.toFixed(2)}
              </p>
            </div>
            <form onSubmit={handleBet} className="space-y-4">
              <div>
                <Label>Select Team</Label>
                <div className="flex gap-4">
                  <Button
                    type="button"
                    variant={teamId === match.team1_id ? "default" : "outline"}
                    onClick={() => setTeamId(match.team1_id)}
                  >
                    Team {match.team1_id}
                  </Button>
                  <Button
                    type="button"
                    variant={teamId === match.team2_id ? "default" : "outline"}
                    onClick={() => setTeamId(match.team2_id)}
                  >
                    Team {match.team2_id}
                  </Button>
                </div>
              </div>
              <div>
                <Label htmlFor="amount">Bet Amount</Label>
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
              <Button type="submit">Place Bet</Button>
            </form>
          </CardContent>
        </Card>
      </motion.div>
    </div>
  );
}
