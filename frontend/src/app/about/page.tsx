import Link from 'next/link';

export default function About() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-center p-4">
      <header className="mb-8">
        <h1 className="text-5xl md:text-7xl font-bold mb-4">
          About Us
        </h1>
        <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
          We are a modern, sleek, and high-performance betting platform.
        </p>
      </header>

      <Link href="/">
        <span className="text-blue-500 hover:underline">
          Go back home
        </span>
      </Link>
    </div>
  );
}
