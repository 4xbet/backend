import { create } from 'zustand';
import { jwtDecode } from 'jwt-decode';

interface DecodedToken {
  id: number;
  sub: string; // 'sub' is the standard JWT claim for subject (often the user's email)
  role: 'user' | 'admin';
}

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
      const decodedToken = jwtDecode<DecodedToken>(token);
      const user: User = {
        id: decodedToken.id,
        email: decodedToken.sub,
        role: decodedToken.role,
      };
      localStorage.setItem('authToken', token);
      set({
        token,
        user,
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
        const decodedToken = jwtDecode<DecodedToken>(token);
        const user: User = {
          id: decodedToken.id,
          email: decodedToken.sub,
          role: decodedToken.role,
        };
        set({
          token,
          user,
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
