import type { Account, Campaign } from "./types";
import { SAMPLE_ACCOUNTS } from "./sample";

const API = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export async function getAccounts(): Promise<Account[]> {
  try {
    const res = await fetch(`${API}/accounts`, { cache: "no-store" });
    return res.ok ? ((await res.json()) as Account[]) : SAMPLE_ACCOUNTS;
  } catch {
    return SAMPLE_ACCOUNTS;
  }
}

export async function runCrew(accountId: string): Promise<Campaign | null> {
  try {
    const res = await fetch(`${API}/run/${accountId}`, { method: "POST" });
    return res.ok ? ((await res.json()) as Campaign) : null;
  } catch {
    return null;
  }
}

export async function approve(accountId: string, approve: boolean): Promise<{ ok: boolean; status?: string; detail?: string }> {
  try {
    const res = await fetch(`${API}/campaign/${accountId}/approve`, {
      method: "POST",
      headers: { "Content-Type": "application/json", "X-Role": "rep" },
      body: JSON.stringify({ approver: "rep:console", approve }),
    });
    if (res.ok) return { ok: true, status: (await res.json()).status };
    const body = await res.json().catch(() => ({}));
    return { ok: false, detail: body.detail ?? `HTTP ${res.status}` };
  } catch {
    return { ok: false, detail: "backend unreachable" };
  }
}
