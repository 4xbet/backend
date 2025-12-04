import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import './global.css';
import ThemeProvider from '@/components/ThemeProvider';
import ThemeSwitcher from '@/components/ui/ThemeSwitcher';
import PageTransition from '@/components/PageTransition';
import { Toaster } from 'react-hot-toast';
import Header from '@/widgets/header/ui/Header';

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: '4xbet Frontend',
  description: 'Modern betting platform',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} bg-background text-foreground transition-colors duration-300`}>
        <ThemeProvider>
          <Toaster position="bottom-right" />
          <Header />
          <main className="container mx-auto p-4">
            <PageTransition>{children}</PageTransition>
          </main>
        </ThemeProvider>
      </body>
    </html>
  );
}
