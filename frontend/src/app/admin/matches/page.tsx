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
} from "@/shared/ui/table";
import { Button } from "@/shared/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/shared/ui/dialog";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/card";
import apiClient from "@/shared/api";
import { Match, Team } from "@/shared/types";
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
      console.error("Failed to fetch matches or teams:", error);
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
    return <div className="text-center py-10">Loading matches...</div>;
  }

  return (
    <div className="container mx-auto py-10">
      <motion.div initial={{ opacity: 0, y: -20 }} animate={{ opacity: 1, y: 0 }}>
        <Card>
          <CardHeader className="flex flex-row items-center justify-between">
            <CardTitle>Manage Matches</CardTitle>
            <Dialog open={isMatchDialogOpen} onOpenChange={setMatchDialogOpen}>
              <DialogTrigger asChild>
                <Button>Add Match</Button>
              </DialogTrigger>
              <DialogContent>
                <DialogHeader>
                  <DialogTitle>Add New Match</DialogTitle>
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
                  <TableHead>Teams</TableHead>
                  <TableHead>Start Time</TableHead>
                  <TableHead>Actions</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {matches.map((match) => (
                  <TableRow key={match.id}>
                    <TableCell>{match.id}</TableCell>
                    <TableCell>
                      {teams.find((t) => t.id === match.team1_id)?.name || "N/A"} vs{" "}
                      {teams.find((t) => t.id === match.team2_id)?.name || "N/A"}
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
                        Edit Odds
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
            <DialogTitle>Edit Odds</DialogTitle>
          </DialogHeader>
          {selectedMatch && <OddsForm match={selectedMatch} onSuccess={handleSuccess} />}
        </DialogContent>
      </Dialog>
    </div>
  );
}
