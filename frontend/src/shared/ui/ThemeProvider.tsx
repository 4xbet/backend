'use client';
import { useEffect, ReactNode } from 'react';
import { useThemeStore } from '@/shared/ui/themeStore';

interface ThemeProviderProps {
  children: ReactNode;
}

const ThemeProvider = ({ children }: ThemeProviderProps) => {
  const initializeTheme = useThemeStore((state) => state.initializeTheme);

  useEffect(() => {
    initializeTheme();
  }, [initializeTheme]);

  return <>{children}</>;
};

export default ThemeProvider;
