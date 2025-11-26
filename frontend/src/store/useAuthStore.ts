import { create } from 'zustand';
import { jwtDecode } from 'jwt-decode';

interface User {
  id: number;
  email: string;
  role: 'user' | 'admin';
}

interface AuthState {
  token: string | null;
  user: User | null;
  isLoggedIn: boolean;
  isLoading: boolean;
  login: (token: string) => void;
  logout: () => void;
  initialize: () => void;
}

const useAuthStore = create<AuthState>((set) => ({
  token: null,
  user: null,
  isLoggedIn: false,
  isLoading: true,
  login: (token) => {
    try {
      const decodedUser = jwtDecode<User>(token);
      localStorage.setItem('authToken', token);
      set({
        token,
        user: decodedUser,
        isLoggedIn: true,
      });
    } catch (error) {
      console.error('Failed to decode token:', error);
    }
  },
  logout: () => {
    localStorage.removeItem('authToken');
    set({
      token: null,
      user: null,
      isLoggedIn: false,
    });
  },
  initialize: () => {
    try {
      const token = localStorage.getItem('authToken');
      if (token) {
        const decodedUser = jwtDecode<User>(token);
        set({
          token,
          user: decodedUser,
          isLoggedIn: true,
          isLoading: false,
        });
      } else {
        set({ isLoading: false });
      }
    } catch (error) {
      console.error('Failed to initialize auth state:', error);
      set({ isLoading: false });
    }
  },
}));

export default useAuthStore;
