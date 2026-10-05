export const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:5000";

export type User = { id: string; name: string; email: string; picture?: string | null };
export type Task = {
  id: string;
  title: string;
  description?: string | null;
  status: "pending" | "completed";
  created_by: string;
  assigned_to: string;
  created_at: string;
};

export async function api<T = void>(path: string, init: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    ...init,
    credentials: "include", // send the Flask session cookie
    headers: { "Content-Type": "application/json", ...init.headers },
  });
  if (!res.ok) {
    const body = await res.json().catch(() => null);
    throw new Error(body?.error ?? (res.status === 401 ? "Please sign in" : "Something went wrong"));
  }
  return (res.status === 204 ? undefined : await res.json()) as T;
}
