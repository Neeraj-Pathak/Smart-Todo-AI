import './globals.css';
import Link from 'next/link';

export const metadata = { title: 'Smart Todo' };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <header className="bg-slate-900 text-white py-3 px-6 flex gap-6">
          <Link href="/">Dashboard</Link>
          <Link href="/new">New Task</Link>
          <Link href="/context">Context</Link>
        </header>
        {children}
      </body>
    </html>
  );
}
