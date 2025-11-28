"use client";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import Link from "next/link";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/card";
import apiClient from "@/shared/api";
import { Match, Team } from "@/shared/types";

export default function MatchesPage() {
  const [matches, setMatches] = useState<Match[]>([]);
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMatchesAndTeams = async () => {
      try {
        const [matchesRes, teamsRes] = await Promise.all([
          apiClient.matches.getAll(),
          apiClient.teams.getAll(),
        ]);
        if (Array.isArray(matchesRes.data)) {
          setMatches(matchesRes.data);
        } else {
          console.error("Fetched matches data is not an array:", matchesRes.data);
        }
        if (Array.isArray(teamsRes.data)) {
          setTeams(teamsRes.data);
        } else {
          console.error("Fetched teams data is not an array:", teamsRes.data);
        }
      } catch (error) {
        console.error("Failed to fetch matches or teams:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchMatchesAndTeams();
  }, []);

  const getTeamName = (teamId: number) => {
    return teams.find((t) => t.id === teamId)?.name || `Team ${teamId}`;
  };

  if (loading) {
    return <div className="text-center py-10">Загрузка матчей...</div>;
  }

  return (
    <div className="container mx-auto py-10">
      <h1 className="text-4xl font-bold mb-8">Предстоящие матчи</h1>
      <motion.div
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
        initial="hidden"
        animate="visible"
        variants={{
          visible: { transition: { staggerChildren: 0.1 } },
          hidden: {},
        }}
      >
        {matches.map((match) => (
          <motion.div
            key={match.id}
            variants={{
              visible: { opacity: 1, y: 0 },
              hidden: { opacity: 0, y: 20 },
            }}
          >
            <Link href={`/matches/${match.id}`} passHref>
              <Card className="hover:shadow-lg transition-shadow duration-300">
                <CardHeader>
                  <CardTitle>{getTeamName(match.team1_id)} vs {getTeamName(match.team2_id)}</CardTitle>
                </CardHeader>
                <CardContent>
                  <p className="text-sm text-gray-500">
                    {new Date(match.start_time).toLocaleString()}
                  </p>
                </CardContent>
              </Card>
            </Link>
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
