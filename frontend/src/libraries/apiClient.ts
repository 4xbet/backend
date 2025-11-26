import axios, { AxiosInstance } from 'axios';
import useAuthStore from '@/store/useAuthStore';
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
} from '@/types';

const axiosInstance: AxiosInstance = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api',
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
    getMe: () => axiosInstance.get<User>('/users/me'),
    getWallet: () => axiosInstance.get<Wallet>('/users/me/wallet'),
    updateWallet: (data: UpdateWalletData) => axiosInstance.patch<Wallet>('/users/me/wallet', data),
    register: (data: any) => axiosInstance.post<User>('/users/', data),
  },
  auth: {
    login: (data: any) =>
      axiosInstance.post('/token', data, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      }),
  },
  teams: {
    create: (data: CreateTeamData) => axiosInstance.post<Team>('/teams/', data),
    getAll: () => axiosInstance.get<Team[]>('/teams/'),
    getById: (id: string) => axiosInstance.get<Team>(`/teams/${id}`),
    update: (id: string, data: UpdateTeamData) => axiosInstance.put<Team>(`/teams/${id}`, data),
    delete: (id: string) => axiosInstance.delete(`/teams/${id}`),
  },
  matches: {
    create: (data: CreateMatchData) => axiosInstance.post<Match>('/matches/', data),
    getAll: () => axiosInstance.get<Match[]>('/matches/'),
    getById: (id: string) => axiosInstance.get<Match>(`/matches/${id}`),
    updateOdds: (id: string, data: UpdateOddsData) => axiosInstance.post(`/matches/${id}/odds`, data),
  },
  bets: {
    create: (data: CreateBetData) => axiosInstance.post<Bet>('/bets/', data),
    getMyBets: () => axiosInstance.get<Bet[]>('/bets/'),
  },
};

export default apiClient;
