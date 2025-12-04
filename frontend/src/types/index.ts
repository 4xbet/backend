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
  home_team_id: number;    // ← Изменено с team1_id
  away_team_id: number;    // ← Изменено с team2_id
  start_time: string;
  status?: string;         // ← Добавлено
  result?: string;         // ← Добавлено
  odds?: any;              // ← Добавлено для коэффициентов
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
  home_team_id: number;    // ← Изменено с team1_id
  away_team_id: number;    // ← Изменено с team2_id
  start_time: string;
}

export interface UpdateOddsData {
  win_home: number;        // ← Изменено с odds_team1
  draw: number;            // ← Добавлено
  win_away: number;        // ← Изменено с odds_team2
}

export interface CreateBetData {
  match_id: number;
  team_id: number;
  amount: number;
}