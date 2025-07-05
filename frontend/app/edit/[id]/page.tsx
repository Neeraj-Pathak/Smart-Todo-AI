'use client';

import { notFound, useRouter, useParams } from 'next/navigation';
import { useEffect, useState } from 'react';
import api from '@/lib/api';

type Task = {
  id: number;
  title: string;
  description: string;
  priority_score: number;
  category: string;
  deadline?: string;
};

export default function EditTask() {
  const router = useRouter();
  const { id } = useParams<{ id: string }>();      // ← safe param access

  const [task, setTask] = useState<Task | null>(null);
  const [ai, setAi] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  /* fetch the task */
  useEffect(() => {
    if (!id) return;
    const fetchTask = async () => {
      try {
        const res = await api.get<Task>(`/tasks/${id}/`);
        setTask(res.data);
      } catch {
        notFound();
      }
    };
    fetchTask();
  }, [id]);

  if (!task) return <p className="p-6">Loading…</p>;

  /* field change */
  const updateField = (
    e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>
  ) => setTask({ ...task, [e.target.name]: e.target.value });

  /* AI suggestion */
  const getAi = async () => {
    setLoading(true);
    const ctx = (await api.get('/context/')).data.map((e: any) => e.content);
    const res = await api.post('/ai/suggestions/', {
      title: task.title,
      description: task.description,
      context: ctx,
    });
    setAi(res.data);
    setTask((prev) => ({
      ...prev!,
      description: res.data.enhanced_description || prev!.description,
    }));
    setLoading(false);
  };

  /* save */
  const saveTask = async () => {
    await api.put(`/tasks/${task.id}/`, {
      ...task,
      priority_score: ai?.priority_score ?? task.priority_score,
      deadline: ai?.suggested_deadline ?? task.deadline,
      category: ai?.suggested_category ?? task.category,
    });
    router.push('/');
  };

  return (
    <main className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Edit Task</h1>

      <label htmlFor="edit-title" className="block mb-2 font-medium">Title</label>
      <input
        id="edit-title"
        type="text"
        name="title"
        value={task.title}
        onChange={updateField}
        className="w-full border rounded p-2 mb-4"
      />

      <label htmlFor="edit-desc" className="block mb-2 font-medium">Description</label>
      <textarea
        id="edit-desc"
        name="description"
        value={task.description}
        onChange={updateField}
        rows={4}
        className="w-full border rounded p-2 mb-4"
      />

      <button
        onClick={getAi}
        className="bg-purple-600 text-white px-4 py-2 rounded-xl mr-3"
      >
        {loading ? 'Thinking…' : 'Get AI Suggestion'}
      </button>

      {ai && (
        <div className="border p-4 rounded-xl mt-4
                        bg-gray-100 text-gray-900
                        dark:bg-slate-800 dark:text-white shadow">
          <p><strong>Priority:</strong> {ai.priority_score}</p>
          <p><strong>Deadline:</strong> {ai.suggested_deadline}</p>
          <p><strong>Category:</strong> {ai.suggested_category}</p>
          <p className="mt-2"><strong>Description:</strong> {ai.enhanced_description}</p>
        </div>
      )}

      <button
        onClick={saveTask}
        className="bg-green-600 text-white px-4 py-2 rounded-xl mt-6"
      >
        Save Task
      </button>
    </main>
  );
}
