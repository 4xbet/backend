"use client";
import Link from "next/link";
import { motion, Variants } from "framer-motion";
import { Card, CardContent, CardHeader, CardTitle } from "@/shared/ui/card";
import { Button } from "@/shared/ui/button";
import { ArrowRight, BarChart2, Ticket, User } from "lucide-react";
import useAuthStore from "@/entities/user/model/store";

export default function HomePage() {
  const { isLoggedIn } = useAuthStore();

  const cardVariants: Variants = {
    hidden: { opacity: 0, y: 50 },
    visible: (i: number) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: i * 0.2,
        duration: 0.5,
        ease: "easeOut",
      },
    }),
  };

  const features = [
    {
      title: "Live Матчи",
      description: "Следите за результатами в реальном времени.",
      href: "/matches",
      icon: <BarChart2 className="h-8 w-8 text-primary" />,
    },
    {
      title: "Ваши Ставки",
      description: "Просматривайте историю и текущие ставки.",
      href: "/my-bets",
      icon: <Ticket className="h-8 w-8 text-primary" />,
    },
    {
      title: "Профиль",
      description: "Управляйте своим аккаунтом и кошельком.",
      href: "/profile",
      icon: <User className="h-8 w-8 text-primary" />,
    },
  ];

  return (
    <div className="container mx-auto text-center py-10">
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="mb-12"
      >
        <h1 className="text-4xl md:text-6xl font-bold mb-4">
          Добро пожаловать в <span className="text-primary">4xBet</span>
        </h1>
        <p className="text-lg md:text-xl text-muted-foreground">
          Ваша платформа для ставок на любимые матчи.
        </p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        {features.map((feature, i) => (
          <motion.div key={feature.title} custom={i} variants={cardVariants} initial="hidden" animate="visible">
            <Card className="h-full flex flex-col">
              <CardHeader className="flex-row items-center gap-4">
                {feature.icon}
                <CardTitle>{feature.title}</CardTitle>
              </CardHeader>
              <CardContent className="flex-grow">
                <p className="text-muted-foreground">{feature.description}</p>
              </CardContent>
              <div className="p-6 pt-0">
                <Link href={feature.href} passHref>
                  <Button className="w-full">
                    Перейти <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
              </div>
            </Card>
          </motion.div>
        ))}
      </div>

      {!isLoggedIn && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8, duration: 0.5 }}
          className="mt-12"
        >
          <p className="text-lg mb-4">Готовы начать?</p>
          <Link href="/register" passHref>
            <Button size="lg">
              Присоединяйтесь сейчас <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          </Link>
        </motion.div>
      )}
    </div>
  );
}
