'use client';

import { useEffect, useState } from 'react';
import { MoreHorizontal } from 'lucide-react';
import toast from 'react-hot-toast';

import AuthGuard from '@/components/AuthGuard';
import { Button } from '@/components/ui/button';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import apiClient from '@/libraries/apiClient';

interface Team {
  id: number;
  name: string;
}

const AdminTeamsPage = () => {
  const [teams, setTeams] = useState<Team[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTeams = async () => {
      try {
        setLoading(true);
        const response = await apiClient.get('/teams/');
        setTeams(response.data);
      } catch (error) {
        toast.error('Failed to fetch teams.');
      } finally {
        setLoading(false);
      }
    };

    fetchTeams();
  }, []);

  const handleDelete = async (id: number) => {
    if (confirm('Are you sure you want to delete this team?')) {
      try {
        await apiClient.delete(`/teams/${id}`);
        setTeams(teams.filter((team) => team.id !== id));
        toast.success('Team deleted successfully.');
      } catch (error) {
        toast.error('Failed to delete team.');
      }
    }
  };

  return (
    <AuthGuard adminOnly>
      <div className="container mx-auto py-10">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">Manage Teams</h1>
          <Button>Add Team</Button>
        </div>
        {loading ? (
          <p>Loading teams...</p>
        ) : (
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>ID</TableHead>
                <TableHead>Name</TableHead>
                <TableHead>
                  <span className="sr-only">Actions</span>
                </TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {teams.map((team) => (
                <TableRow key={team.id}>
                  <TableCell className="font-medium">{team.id}</TableCell>
                  <TableCell>{team.name}</TableCell>
                  <TableCell>
                    <DropdownMenu>
                      <DropdownMenuTrigger asChild>
                        <Button aria-haspopup="true" size="icon" variant="ghost">
                          <MoreHorizontal className="h-4 w-4" />
                          <span className="sr-only">Toggle menu</span>
                        </Button>
                      </DropdownMenuTrigger>
                      <DropdownMenuContent align="end">
                        <DropdownMenuLabel>Actions</DropdownMenuLabel>
                        <DropdownMenuItem>Edit</DropdownMenuItem>
                        <DropdownMenuItem onClick={() => handleDelete(team.id)}>Delete</DropdownMenuItem>
                      </DropdownMenuContent>
                    </DropdownMenu>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </AuthGuard>
  );
};

export default AdminTeamsPage;
