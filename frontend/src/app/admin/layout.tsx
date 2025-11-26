"use client";
import { useEffect } from "react";
import { useRouter } from "next/navigation";
import useAuthStore from "@/store/useAuthStore";

export default function AdminLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const { user, isLoggedIn, isLoading } = useAuthStore();

  useEffect(() => {
    if (!isLoading && (!isLoggedIn || user?.role !== "admin")) {
      router.replace("/matches");
    }
  }, [user, isLoggedIn, isLoading, router]);

  if (isLoading || !isLoggedIn || user?.role !== "admin") {
    return <div className="text-center py-10">Loading...</div>;
  }

  return <div>{children}</div>;
}
