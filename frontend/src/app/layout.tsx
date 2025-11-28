import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./global.css";
import ThemeProvider from "@/shared/ui/ThemeProvider";
import ThemeSwitcher from "@/shared/ui/ThemeSwitcher";
import PageTransition from "@/shared/ui/PageTransition";
import { Toaster } from 'react-hot-toast'; // Import Toaster
import Header from "@/widgets/header/ui/Header";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "4xbet Frontend",
  description: "Modern betting platform",
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
          <main className="container mx-auto py-8">
            <PageTransition>{children}</PageTransition>
          </main>
        </ThemeProvider>
      </body>
    </html>
  );
}
