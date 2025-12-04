import { create } from 'zustand';
import { jwtDecode } from 'jwt-decode';

interface User {
  id: number;
  email: string;
  role: 'user' | 'admin';
}

interface DecodedToken {
  sub: string;
  role: 'user' | 'admin';
  id: number;
  exp: number;
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
  
  login: (token: string) => {
    try {
      const decoded = jwtDecode<DecodedToken>(token);
      const user: User = {
        id: decoded.id,
        email: decoded.sub,
        role: decoded.role,
      };
      
      localStorage.setItem('authToken', token);
      
      set({
        token,
        user,
        isLoggedIn: true,
        isLoading: false,
      });
    } catch (error) {
      console.error('Failed to decode token:', error);
      set({ isLoading: false });
    }
  },
  
  logout: () => {
    localStorage.removeItem('authToken');
    set({
      token: null,
      user: null,
      isLoggedIn: false,
      isLoading: false,
    });
  },
  
  initialize: () => {
    try {
      if (typeof window === 'undefined') {
        set({ isLoading: false });
        return;
      }
      
      const token = localStorage.getItem('authToken');
      if (token) {
        const decoded = jwtDecode<DecodedToken>(token);
        const user: User = {
          id: decoded.id,
          email: decoded.sub,
          role: decoded.role,
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
