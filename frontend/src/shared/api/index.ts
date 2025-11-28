import axios, { AxiosInstance } from 'axios';
import useAuthStore from '@/entities/user/model/store';
import {
  Bet,
  CreateBetData,
  CreateMatchData,
  CreateTeamData,
  Match,
  Team,
  UpdateOddsData,
  UpdateTeamData,
  UpdateWalletData,
  User,
  Wallet,
} from '@/shared/types';

const axiosInstance: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

axiosInstance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  },
);

axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  },
);

const apiClient = {
  users: {
    getMe: () => axiosInstance.get<User>('/api/users/me'),
    getWallet: () => axiosInstance.get<Wallet>('/api/users/me/wallet'),
    updateWallet: (data: UpdateWalletData) => axiosInstance.patch<Wallet>('/api/users/me/wallet', data),
    register: (data: any) => axiosInstance.post<User>('/api/users/', data),
  },
  auth: {
    login: (data: any) =>
      axiosInstance.post('/api/token', data, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      }),
  },
  teams: {
    create: (data: CreateTeamData) => axiosInstance.post<Team>('/api/teams/', data),
    getAll: () => axiosInstance.get<Team[]>('/api/teams/'),
    getById: (id: string) => axiosInstance.get<Team>(`/api/teams/${id}`),
    update: (id: string, data: UpdateTeamData) => axiosInstance.put<Team>(`/api/teams/${id}`, data),
    delete: (id: string) => axiosInstance.delete(`/api/teams/${id}`),
  },
  matches: {
    create: (data: CreateMatchData) => axiosInstance.post<Match>('/api/matches/', data),
    getAll: () => axiosInstance.get<Match[]>('/api/matches/'),
    getById: (id: string) => axiosInstance.get<Match>(`/api/matches/${id}`),
    updateOdds: (id: string, data: UpdateOddsData) => axiosInstance.post(`/api/matches/${id}/odds`, data),
  },
  bets: {
    create: (data: CreateBetData) => axiosInstance.post<Bet>('/api/bets/', data),
    getMyBets: () => axiosInstance.get<Bet[]>('/api/bets/'),
  },
};

export default apiClient;
