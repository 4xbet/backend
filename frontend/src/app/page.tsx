import AnimatedButton from "@/components/ui/AnimatedButton";
import Link from "next/link";

export default function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-center p-4">
      <header className="mb-8">
        <h1 className="text-5xl md:text-7xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-gray-700 via-gray-900 to-black dark:from-gray-100 dark:via-gray-300 dark:to-white">
          Welcome to 4xbet
        </h1>
        <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
          The modern, sleek, and high-performance frontend for your betting platform.
          Built with Next.js, Tailwind CSS, and Framer Motion.
        </p>
      </header>

      <div className="flex flex-col sm:flex-row gap-4">
        <AnimatedButton className="bg-blue-600 hover:bg-blue-700 dark:bg-blue-500 dark:hover:bg-blue-600 text-white">
          Get Started
        </AnimatedButton>
        <Link href="/about">
          <AnimatedButton>
            Learn More
          </AnimatedButton>
        </Link>
      </div>

      <footer className="absolute bottom-8 text-gray-500 dark:text-gray-400">
        <p>Toggle the theme using the switch in the top-right corner.</p>
      </footer>
    </div>
  );
}
