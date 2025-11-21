export interface User {
  id: number;
  email: string;
  role: 'user' | 'admin';
}

export interface Wallet {
  balance: number;
}

export interface Team {
  id: number;
  name: string;
}

export interface Match {
  id: number;
  team1_id: number;
  team2_id: number;
  start_time: string;
}

export interface Bet {
  id: number;
  match_id: number;
  team_id: number;
  amount: number;
  status: string;
}

// API Payloads
export interface RegisterData {
  email: string;
  password: string;
}

export interface UpdateWalletData {
  amount: number;
}

export interface CreateTeamData {
  name: string;
}

export interface UpdateTeamData {
  name: string;
}

export interface CreateMatchData {
  team1_id: number;
  team2_id: number;
  start_time: string;
}

export interface UpdateOddsData {
  odds_team1: number;
  odds_team2: number;
}

export interface CreateBetData {
  match_id: number;
  team_id: number;
  amount: number;
}
