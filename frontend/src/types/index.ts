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
  home_team_id: number;    
  away_team_id: number;  
  start_time: string;
  status?: string;         
  result?: string;         
  odds?: any;             
}

export interface Bet {
  id: number;
  match_id: number;
  team_id: number;
  amount: number;
  status: string;
}


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
  home_team_id: number;    
  away_team_id: number;    
  start_time: string;
}

export interface UpdateOddsData {
  win_home: number;        
  draw: number;            
  win_away: number;        
}

export interface CreateBetData {
  match_id: number;
  outcome: string;      
  amount_staked: number; 
}

export interface Bet {
  id: number;
  match_id: number;
  outcome: string;      
  amount_staked: number; 
  status: string;
  odds_on_bet?: number;
  user_id?: number;
  created_at?: string;
}