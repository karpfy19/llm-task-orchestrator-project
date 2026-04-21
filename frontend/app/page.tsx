"use client";

import { useEffect, useState } from "react";

type Task = {
  id: string;
  name: string;
  prompt: string;
  status: string;
  output?: string;
  error?: string;
  created_at?: string;
  scheduled_at?: string;
};

const API = process.env.NEXT_PUBLIC_API_URL;

export default function Home() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [selectedTask, setSelectedTask] = useState<Task | null>(null);

  const [name, setName] = useState("");
  const [prompt, setPrompt] = useState("");
  const [scheduledAt, setScheduledAt] = useState("");

  const [loading, setLoading] = useState(false);

  // -----------------------
  // Fetch tasks
  // -----------------------
  const loadTasks = async () => {
    const res = await fetch(`${API}/tasks`);
    const data = await res.json();
    setTasks(data);
  };

  useEffect(() => {
    loadTasks();

    // UX improvement #3: auto-refresh polling UI
    const interval = setInterval(loadTasks, 3000);
    return () => clearInterval(interval);
  }, []);

  // -----------------------
  // Create task
  // -----------------------
  const createTask = async () => {
    setLoading(true);

    await fetch(`${API}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name,
        prompt,
        scheduled_at: scheduledAt || null,
      }),
    });

    setName("");
    setPrompt("");
    setScheduledAt("");

    await loadTasks();
    setLoading(false);
  };

  // -----------------------
  // Load single task
  // -----------------------
  const openTask = async (id: string) => {
    const res = await fetch(`${API}/tasks/${id}`);
    const data = await res.json();
    setSelectedTask(data);
  };

  // -----------------------
  // Chain task
  // -----------------------
  const chainTask = async (task: Task) => {
    await fetch(`${API}/tasks`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        name: `Follow-up: ${task.name}`,
        prompt: task.output || task.prompt,
        parent_task_id: task.id,
      }),
    });

    loadTasks();
  };

  // -----------------------
  // Status color helper (UX #4)
  // -----------------------
  const statusColor = (status: string) => {
    if (status === "COMPLETED") return "green";
    if (status === "FAILED") return "red";
    if (status === "RUNNING") return "orange";
    return "gray";
  };

  return (
    <div style={{ display: "flex", padding: 20, gap: 20, fontFamily: "sans-serif" }}>
      {/* LEFT: Create Task */}
      <div style={{ width: "30%" }}>
        <h2>Create Task</h2>

        <input
          placeholder="Name"
          value={name}
          onChange={(e) => setName(e.target.value)}
          style={{ width: "100%", marginBottom: 10 }}
        />

        <textarea
          placeholder="Prompt"
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          style={{ width: "100%", height: 100, marginBottom: 10 }}
        />

        <input
          placeholder="Schedule (ISO optional)"
          value={scheduledAt}
          onChange={(e) => setScheduledAt(e.target.value)}
          style={{ width: "100%", marginBottom: 10 }}
        />

        {/* UX #2: disabled + loading state */}
        <button onClick={createTask} disabled={loading}>
          {loading ? "Creating..." : "Create Task"}
        </button>

        {/* UX #5: empty state */}
        {tasks.length === 0 && (
          <p style={{ marginTop: 10 }}>No tasks yet</p>
        )}
      </div>

      {/* CENTER: Task list */}
      <div style={{ width: "35%" }}>
        <h2>Tasks</h2>

        <button onClick={loadTasks}>Refresh</button>

        <ul>
          {tasks.map((t) => (
            <li key={t.id} style={{ marginBottom: 12 }}>
              <div>
                <b>{t.name}</b>
              </div>

              {/* UX #4: status color indicator */}
              <div>
                Status:{" "}
                <span style={{ color: statusColor(t.status) }}>
                  {t.status}
                </span>
              </div>

              <button onClick={() => openTask(t.id)}>View</button>

              {/* UX #7: disable chaining unless valid */}
              <button
                onClick={() => chainTask(t)}
                disabled={t.status !== "COMPLETED"}
              >
                Chain
              </button>
            </li>
          ))}
        </ul>
      </div>

      {/* RIGHT: Task detail */}
      <div style={{ width: "35%" }}>
        <h2>Task Detail</h2>

        {/* UX #6: fallback state */}
        {selectedTask ? (
          <div>
            <h3>{selectedTask.name}</h3>

            <p>Status: {selectedTask.status}</p>

            <h4>Prompt</h4>
            <pre>{selectedTask.prompt}</pre>

            <h4>Output</h4>
            <pre>{selectedTask.output || "No output yet"}</pre>

            {selectedTask.error && (
              <>
                <h4>Error</h4>
                <pre style={{ color: "red" }}>{selectedTask.error}</pre>
              </>
            )}
          </div>
        ) : (
          <p>Select a task to view details</p>
        )}
      </div>
    </div>
  );
}