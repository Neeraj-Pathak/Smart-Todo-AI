'use client';

import { useEffect, useState } from 'react';
import api from '../../lib/api'; 

interface ContextEntry {
  id: number;
  content: string;
  source_type: string;
  timestamp: string;
}

export default function ContextPage() {
  const [content, setContent] = useState('');
  const [list, setList] = useState<ContextEntry[]>([]);

  const fetch = async () => {
    try {
      const res = await api.get<ContextEntry[]>('/context/');
      
      setList(res.data);
    } catch (err) {
      console.error('Error fetching context:', err);
    }
  };

  useEffect(() => {
    fetch();
  }, []);

  const addContext = async () => {
    if (!content.trim()) return;

    try {
      await api.post('/context/', {
        content: content.trim(),
        source_type: 'NT' // hardcoded to "Note"
      });
      setContent('');
      fetch();
    } catch (err: any) {
      console.error('Context save failed:', err.response?.data || err.message);
      alert("Failed to save context\n" + JSON.stringify(err.response?.data));
    }
  };

  return (
    <main className="p-6 max-w-3xl mx-auto">
      <h1 className="text-2xl font-bold mb-4">Add Daily Context</h1>

      <textarea
        value={content}
        onChange={(e) => setContent(e.target.value)}
        rows={3}
        className="w-full border rounded p-2 mb-3"
        placeholder="Paste an email, chat, or note…"
      />

      <button
        onClick={addContext}
        className="bg-blue-600 text-white px-4 py-2 rounded-xl"
      >
        Save Context
      </button>

      <h2 className="text-xl font-semibold mt-8 mb-3">History</h2>
      <ul className="space-y-3">
        {list.map((c) => (
          <li
            key={c.id}
            className="border rounded p-3 bg-gray-100 text-gray-900 dark:bg-slate-800 dark:text-white shadow"
          >
            {c.content}
            <span className="block text-xs mt-1 text-gray-600 dark:text-gray-300">
              {new Date(c.timestamp).toLocaleString()}
            </span>
          </li>
        ))}
      </ul>
    </main>
  );
}
