import Link from 'next/link';

export default function About() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-center p-4">
      <header className="mb-8">
        <h1 className="text-5xl md:text-7xl font-bold mb-4">
          О нас
        </h1>
        <p className="text-lg md:text-xl text-gray-600 dark:text-gray-300 max-w-2xl mx-auto">
          Мы — современная, стильная и высокопроизводительная платформа для ставок.
        </p>
      </header>

      <Link href="/">
        <span className="text-blue-500 hover:underline">
          Вернуться на главную
        </span>
      </Link>
    </div>
  );
}
