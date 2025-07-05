'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

/* ---------- Types ---------- */
interface Task {
  id: number;
  title: string;
  description: string;
  priority_score: number;
  category: string | null;
  deadline?: string;
}

/* ---------- Component ---------- */
export default function Dashboard() {
  const router = useRouter();

  /* state */
  const [tasks, setTasks] = useState<Task[]>([]);
  const [quickTitle, setQuickTitle] = useState('');
  const [priorityFilter, setPriorityFilter] = useState('');  // ← only priority

  /* fetch tasks */
  const fetchTasks = async () => {
    const res = await api.get<Task[]>('/tasks/');
    setTasks(res.data);
  };
  useEffect(() => { fetchTasks(); }, []);

  /* quick add */
  const handleQuickAdd = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!quickTitle.trim()) return;

    try {
      await api.post('/tasks/', { title: quickTitle.trim() });
      setQuickTitle('');
      fetchTasks();
    } catch (err: any) {
      console.error(err.response?.data || err.message);
      alert('Error creating task');
    }
  };
  const getPriorityColor = (score: number) => {
    if (score >= 8) return 'bg-red-600';
    if (score >= 5) return 'bg-yellow-500';
    return 'bg-green-600';
  };
  
  /* delete handler */
  const handleDelete = async (id: number) => {
    if (!confirm('Delete this task?')) return;
    await api.delete(`/tasks/${id}/`);
    setTasks((prev) => prev.filter((t) => t.id !== id));
  };

  /* filtering by priority only */
  const visibleTasks = tasks.filter((t) => {
    if (priorityFilter === 'high' && t.priority_score < 8) return false;
    if (priorityFilter === 'med'  && (t.priority_score < 5 || t.priority_score >= 8)) return false;
    if (priorityFilter === 'low'  && t.priority_score >= 5) return false;
    return true;
  });

  return (
    <main className="max-w-3xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-6">Smart Todo Dashboard</h1>

      {/* Quick‑add */}
      <form onSubmit={handleQuickAdd} className="flex gap-2 mb-6">
        <input
          className="flex-1 border rounded p-2"
          placeholder="Quick add task…"
          value={quickTitle}
          onChange={(e) => setQuickTitle(e.target.value)}
        />
        <button className="bg-blue-600 text-white px-4 rounded">+</button>
      </form>

      {/* Priority Filter */}
      <div className="mb-6">
        <label className="text-sm font-medium">
          Priority&nbsp;
          <select
            className="border rounded p-2 bg-white text-gray-900
                       dark:bg-slate-700 dark:text-white"
            value={priorityFilter}
            onChange={(e) => setPriorityFilter(e.target.value)}
          >
            <option value="">Any</option>
            <option value="high">High (≥ 8)</option>
            <option value="med">Medium (5 – 7.9)</option>
            <option value="low">Low (&lt; 5)</option>
          </select>
        </label>
      </div>

      {/* Task list */}
      <ul className="space-y-4">
        {visibleTasks.map((t) => (
          <li
            key={t.id}
            className="border rounded p-4 shadow
                       bg-white text-gray-900
                       dark:bg-slate-800 dark:text-white"
          >
            <div className="flex justify-between items-start mb-1">
              <div className="flex items-center gap-2">
                <button
                  onClick={() => router.push(`/edit/${t.id}`)}
                  className="text-xs px-2 py-1 rounded bg-amber-500 text-white hover:bg-amber-600"
                >
                  Edit
                </button>
                <button
                  onClick={() => handleDelete(t.id)}
                  className="text-xs px-2 py-1 rounded bg-red-600 text-white hover:bg-red-700"
                >
                  Del
                </button>
                <Link href={`/edit/${t.id}`} className="font-semibold hover:underline">
                  {t.title}
                </Link>
              </div>
              <span className={`text-sm px-2 py-1 rounded-full text-white ${getPriorityColor(t.priority_score)}`}>
  {t.priority_score.toFixed(1)}
</span>

            </div>

            <p className="text-sm mb-1">{t.description}</p>

            {t.deadline && (
              <span className="text-xs text-gray-600 dark:text-gray-300">
                Due {t.deadline}
              </span>
            )}
          </li>
        ))}
      </ul>
    </main>
  );
}
