import type { CampaignStatus, Tier } from "@/lib/types";

const TIER: Record<Tier, string> = {
  A: "bg-emerald-950 text-emerald-300 border border-emerald-800",
  B: "bg-sky-950 text-sky-300 border border-sky-800",
  C: "bg-amber-950 text-amber-300 border border-amber-900",
  disqualified: "bg-slate-800 text-slate-500",
};

const STATUS: Record<CampaignStatus, string> = {
  disqualified: "bg-slate-800 text-slate-500",
  awaiting_approval: "bg-amber-950 text-amber-300 border border-amber-900",
  approved: "bg-emerald-950 text-emerald-300 border border-emerald-800",
  rejected: "bg-red-950 text-red-300 border border-red-800",
};

export function TierBadge({ tier }: { tier: Tier }) {
  return <span className={`pill ${TIER[tier]}`}>tier {tier}</span>;
}

export function StatusBadge({ status }: { status: CampaignStatus }) {
  return <span className={`pill ${STATUS[status]}`}>{status.replace(/_/g, " ")}</span>;
}
