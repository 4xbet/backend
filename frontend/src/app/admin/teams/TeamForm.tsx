"use client";
import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/shared/ui/dialog";
import { Button } from "@/shared/ui/button";
import { Input } from "@/shared/ui/input";
import { Label } from "@/shared/ui/label";
import apiClient from "@/shared/api";
import toast from "react-hot-toast";
import { Team } from "@/shared/types";

interface TeamFormProps {
  team?: Team;
  onSuccess: () => void;
}

export default function TeamForm({ team, onSuccess }: TeamFormProps) {
  const [name, setName] = useState(team?.name || "");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      if (team) {
        await apiClient.teams.update(team.id.toString(), { name });
        toast.success("Team updated successfully!");
      } else {
        await apiClient.teams.create({ name });
        toast.success("Team created successfully!");
      }
      onSuccess();
    } catch (error) {
      toast.error("Failed to save team.");
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <Label htmlFor="name">Team Name</Label>
        <Input
          id="name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
        />
      </div>
      <Button type="submit">{team ? "Update" : "Create"}</Button>
    </form>
  );
}
