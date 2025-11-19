import { create } from 'zustand';

interface ThemeState {
  isDarkMode: boolean;
  toggleTheme: () => void;
}

export const useThemeStore = create<ThemeState>((set) => ({
  isDarkMode: false, // Default theme is light
  toggleTheme: () => set((state) => ({ isDarkMode: !state.isDarkMode })),
}));
