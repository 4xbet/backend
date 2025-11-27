"use client";
import { motion } from "framer-motion";
import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-center p-4 overflow-hidden">
      <motion.div
        initial={{ opacity: 0, y: -50 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeInOut" }}
        className="mb-8"
      >
        <h1 className="text-5xl md:text-7xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-gray-700 via-gray-900 to-black dark:from-gray-100 dark:via-gray-300 dark:to-white">
          Добро пожаловать в 4xbet
        </h1>
        <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
          Ваше идеальное место для ставок на спорт.
        </p>
      </motion.div>

      <motion.div
        initial={{ opacity: 0, scale: 0.8 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5, delay: 0.5, ease: "backOut" }}
        className="flex flex-col sm:flex-row gap-4"
      >
        <Link href="/register" passHref>
          <Button size="lg">Начать</Button>
        </Link>
        <Link href="/login" passHref>
          <Button size="lg" variant="outline">
            Войти
          </Button>
        </Link>
      </motion.div>
    </div>
  );
}
