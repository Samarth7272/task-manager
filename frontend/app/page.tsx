"use client";

import { FormEvent, useCallback, useEffect, useState } from "react";
import { API, api, Task, User } from "@/lib/api";

export default function Home() {
  const [me, setMe] = useState<User | null>(null);
  const [users, setUsers] = useState<User[]>([]);
  const [tasks, setTasks] = useState<Task[]>([]);
  const [ready, setReady] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    try {
      const [u, all, t] = await Promise.all([
        api<User>("/api/me"),
        api<User[]>("/api/users"),
        api<Task[]>("/api/tasks"),
      ]);
      setMe(u);
      setUsers(all);
      setTasks(t);
    } catch {
      setMe(null); // not signed in
    } finally {
      setReady(true);
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const nameOf = (id: string) => (id === me?.id ? "you" : users.find((u) => u.id === id)?.name ?? "Unknown");

  async function createTask(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    const form = e.currentTarget;
    const data = new FormData(form);
    setSaving(true);
    setError("");
    try {
      await api<Task>("/api/tasks", {
        method: "POST",
        body: JSON.stringify({
          title: data.get("title"),
          description: data.get("description"),
          assigned_to: data.get("assigned_to"),
        }),
      });
      form.reset();
      await refresh();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSaving(false);
    }
  }

  async function complete(id: string) {
    setError("");
    try {
      await api(`/api/tasks/${id}/complete`, { method: "PATCH" });
      await refresh();
    } catch (err) {
      setError((err as Error).message);
    }
  }

  async function logout() {
    await api("/auth/logout", { method: "POST" });
    setMe(null);
  }

  if (!ready) return <main className="wrap"><p className="muted">Loading…</p></main>;

  if (!me)
    return (
      <main className="wrap login">
        <h1>Task Manager</h1>
        <p className="muted">Create tasks, assign them to teammates, and get an email when work is added and finished.</p>
        <a className="btn" href={`${API}/auth/login`}>Continue with Google</a>
      </main>
    );

  return (
    <main className="wrap">
      <header className="top">
        <div className="who">
          {me.picture && <img src={me.picture} alt="" width={32} height={32} referrerPolicy="no-referrer" />}
          <span>{me.name}</span>
        </div>
        <button className="link" onClick={logout}>Sign out</button>
      </header>

      <form className="new" onSubmit={createTask}>
        <input name="title" placeholder="What needs doing?" required maxLength={120} />
        <textarea name="description" placeholder="Details (optional)" rows={2} />
        <div className="row">
          <label>
            Assign to
            <select name="assigned_to" defaultValue={me.id}>
              {users.map((u) => (
                <option key={u.id} value={u.id}>{u.id === me.id ? `${u.name} (you)` : u.name}</option>
              ))}
            </select>
          </label>
          <button className="btn" disabled={saving}>{saving ? "Creating…" : "Create task"}</button>
        </div>
        {error && <p className="error" role="alert">{error}</p>}
      </form>

      <ul className="tasks">
        {tasks.length === 0 && <li className="muted">No tasks yet. Create your first one above.</li>}
        {tasks.map((t) => (
          <li key={t.id} className={t.status}>
            <button
              className="check"
              aria-label={`Mark "${t.title}" as complete`}
              disabled={t.status === "completed"}
              onClick={() => complete(t.id)}
            />
            <div>
              <strong>{t.title}</strong>
              {t.description && <p>{t.description}</p>}
              <small className="muted">Assigned to {nameOf(t.assigned_to)} by {nameOf(t.created_by)}</small>
            </div>
          </li>
        ))}
      </ul>
    </main>
  );
}
