"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import type { Campaign } from "@/lib/types";
import { approve as approveApi, runCrew } from "@/lib/api";
import { StatusBadge, TierBadge } from "@/components/badges";

export default function CampaignPage() {
  const { id } = useParams<{ id: string }>();
  const [campaign, setCampaign] = useState<Campaign | null>(null);
  const [loading, setLoading] = useState(true);
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    let live = true;
    setLoading(true);
    runCrew(id).then((c) => {
      if (!live) return;
      setCampaign(c);
      setLoading(false);
    });
    return () => {
      live = false;
    };
  }, [id]);

  async function decide(ok: boolean) {
    const res = await approveApi(id, ok);
    if (res.ok && campaign) {
      setCampaign({ ...campaign, status: (res.status as Campaign["status"]) ?? campaign.status });
      setNotice(null);
    } else {
      setNotice(`Blocked: ${res.detail}`);
    }
  }

  return (
    <main>
      <Link href="/" className="text-sm text-slate-400 hover:text-white">
        ← accounts
      </Link>

      {loading && <p className="mt-6 text-slate-400">Running the crew…</p>}
      {!loading && !campaign && (
        <div className="card mt-6 text-slate-300">
          Needs the backend. Start it with <code className="text-sky-300">sdr serve</code>, then reload.
        </div>
      )}

      {campaign && (
        <div className="mt-4 space-y-5">
          <div className="card">
            <div className="flex flex-wrap items-center gap-2">
              <span className="font-mono text-xs text-slate-500">{campaign.account_id}</span>
              <TierBadge tier={campaign.qualification.tier} />
              <StatusBadge status={campaign.status} />
              <span className="pill bg-slate-800 text-slate-400">fit {campaign.qualification.fit_score}/100</span>
            </div>
            <h1 className="mt-3 text-lg font-semibold text-white">{campaign.company}</h1>
            <ul className="mt-2 space-y-1 text-sm text-slate-400">
              {campaign.qualification.reasons.map((r, i) => (
                <li key={i}>· {r}</li>
              ))}
            </ul>
          </div>

          {campaign.status === "disqualified" && (
            <div className="card text-slate-400">Outside the ICP. No outreach was drafted.</div>
          )}

          {campaign.draft && (
            <div className="card">
              <p className="text-xs uppercase tracking-wide text-slate-500">Subject</p>
              <p className="font-medium text-white">{campaign.draft.subject}</p>
              <div className="mt-3 space-y-2">
                {campaign.draft.claims.map((c, i) => (
                  <p key={i} className="text-sm text-slate-200">
                    {c.text}
                    {c.fact_id ? (
                      <span className="ml-2 text-xs text-emerald-400">grounded · {c.fact_id}</span>
                    ) : (
                      <span className="ml-2 text-xs text-red-400">ungrounded</span>
                    )}
                  </p>
                ))}
                <p className="text-sm text-slate-400">{campaign.draft.cta}</p>
              </div>
              {campaign.review && (
                <p className={`mt-3 text-xs ${campaign.review.grounded ? "text-emerald-400" : "text-red-400"}`}>
                  {campaign.review.note}
                </p>
              )}
            </div>
          )}

          {campaign.status === "awaiting_approval" && (
            <div className="card">
              <p className="mb-1 text-sm font-semibold text-white">Approval to send</p>
              <p className="mb-3 text-xs text-slate-500">Nothing is sent until a rep approves it. Ungrounded outreach cannot be sent.</p>
              {notice && <p className="mb-3 rounded-lg border border-amber-900 bg-amber-950 px-3 py-2 text-sm text-amber-300">{notice}</p>}
              <div className="flex gap-2">
                <button onClick={() => decide(true)} className="rounded-md bg-emerald-700 px-3 py-1.5 text-sm text-white">
                  Approve &amp; send
                </button>
                <button onClick={() => decide(false)} className="rounded-md border border-edge px-3 py-1.5 text-sm text-slate-200">
                  Reject
                </button>
              </div>
            </div>
          )}
        </div>
      )}
    </main>
  );
}
