import Link from "next/link";
import { getAccounts } from "@/lib/api";

export const dynamic = "force-dynamic";

export default async function Home() {
  const accounts = await getAccounts();
  return (
    <main>
      <section className="mb-8">
        <h1 className="text-2xl font-semibold text-white">Target accounts</h1>
        <p className="mt-1 max-w-2xl text-sm text-slate-400">
          A crew of four agents researches each account, qualifies it against the ICP, and drafts outreach
          where every claim is grounded in a fact. Off-ICP accounts are disqualified, and nothing is sent
          without a rep approving it.
        </p>
      </section>

      <div className="grid gap-3 sm:grid-cols-2">
        {accounts.map((a) => (
          <Link key={a.id} href={`/accounts/${a.id}`} className="card transition hover:border-slate-500">
            <div className="flex items-center justify-between">
              <span className="font-mono text-xs text-slate-500">{a.id}</span>
              <span className="pill bg-slate-800 text-slate-400">{a.industry}</span>
            </div>
            <h2 className="mt-2 font-medium text-white">{a.company}</h2>
            <p className="mt-1 text-xs text-slate-500">
              {a.employees} employees · {a.region}
            </p>
          </Link>
        ))}
      </div>
    </main>
  );
}
