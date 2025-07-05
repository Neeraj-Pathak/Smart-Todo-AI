'use client';

import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import api from '@/lib/api';

type FormFields = { title: string; description: string };

export default function NewTask() {
  const router = useRouter();
  const [form, setForm] = useState<FormFields>({ title: '', description: '' });
  const [ai, setAi] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  /* handle input changes */
  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  /* call AI with daily context */
  const getAi = async () => {
    setLoading(true);
    const ctx = (await api.get('/context/')).data.map((e: any) => e.content);
    const res = await api.post('/ai/suggestions/', { ...form, context: ctx });
    setAi(res.data);
    setForm((f) => ({ ...f, description: res.data.enhanced_description || f.description }));
    setLoading(false);
  };

  /* save task */
  const saveTask = async () => {
  try {
    await api.post('/tasks/', {
      title: form.title.trim(),
      description: ai?.enhanced_description || form.description.trim(),
      priority_score: ai?.priority_score ?? 5,
      deadline: ai?.suggested_deadline,      // can be null
      // category: 1                        // add if serializer still needs ID
    });
    router.push('/');
  } catch (err: any) {
    console.error('Save‑task error:', err.response?.data || err.message);
    alert(JSON.stringify(err.response?.data, null, 2));   // pop‑up to see details
  }
};
<button disabled={loading} className={`px-4 py-2 rounded-xl ${loading ? 'bg-gray-400' : 'bg-purple-600 text-white'}`}>
  {loading ? 'Thinking…' : 'Get AI Suggestion'}
</button>


  return (
    <main className="p-6 max-w-xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Create New Task</h1>

      <label htmlFor="task-title" className="block mb-2 font-medium">Title</label>
      <input
        id="task-title"
        type="text"
        name="title"
        value={form.title}
        onChange={handleChange}
        className="w-full border rounded p-2 mb-4"
        placeholder="Enter task title"
      />

      <label htmlFor="task-desc" className="block mb-2 font-medium">Description</label>
      <textarea
        id="task-desc"
        name="description"
        value={form.description}
        onChange={handleChange}
        rows={4}
        className="w-full border rounded p-2 mb-4"
        placeholder="Optional: describe the task"
      />

      <button
        onClick={getAi}
        className="bg-purple-600 text-white px-4 py-2 rounded-xl mr-3"
      >
        {loading ? 'Thinking…' : 'Get AI Suggestion'}
      </button>

      {ai && (
        <div className="border p-4 rounded-xl mt-4
                        bg-gray-100 text-gray-900
                        dark:bg-slate-800 dark:text-white shadow">
          <p><strong>Priority:</strong> {ai.priority_score}</p>
          <p><strong>Suggested Deadline:</strong> {ai.suggested_deadline}</p>
          <p><strong>Category Suggestion:</strong> {ai.suggested_category}</p>
          <p className="mt-2"><strong>Enhanced Description:</strong> {ai.enhanced_description}</p>

          <button
            onClick={saveTask}
            className="bg-green-600 text-white px-4 py-2 rounded-xl mt-4"
          >
            Save Task
          </button>
        </div>
      )}
    </main>
  );
}
