'use client';
import { Moon, Sun } from 'lucide-react';
import { Button } from '@/shared/ui/button';
import { useThemeStore } from '@/shared/ui/themeStore';

const ThemeSwitcher = () => {
  const { theme, toggleTheme } = useThemeStore();

  return (
    <Button variant="ghost" size="icon" onClick={toggleTheme} aria-label="Toggle theme">
      {theme === 'dark' ? <Sun className="size-5" /> : <Moon className="size-5" />}
    </Button>
  );
};

export default ThemeSwitcher;
