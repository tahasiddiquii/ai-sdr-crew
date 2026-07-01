# AGENTS.md

Working notes for anyone (human or agent) changing this repo.

## What this is

An AI sales-development crew, full stack. Four agents (researcher, qualifier, writer, reviewer)
collaborate to research an account, qualify it against an ICP, and draft outreach where every claim is
grounded in a fact. Off-ICP accounts are disqualified; nothing is sent without a rep approving it.
Offline by default; `SDR_PROVIDER=openai` swaps in a real CrewAI crew for the writing step.

## Golden rules

- **No fabrication.** Every claim about an account must cite a real fact id. The reviewer enforces it,
  and a draft with any ungrounded claim cannot be approved (`crew.approve` raises `UngroundedError`).
  The eval asserts zero ungrounded claims across all drafts.
- **No auto-send.** `Crew.run` never returns `approved`; a rep must approve. The eval asserts zero
  auto-approvals.
- **Disqualify, do not force-fit.** An off-ICP account is disqualified with reasons, and gets no
  outreach. Wasting a rep's time on a bad lead is a real cost.
- **Offline, deterministic, zero-key by default.** The crew runs with no keys. Keep it that way; the
  real CrewAI path is guarded behind the provider switch.

## Layout

```
backend/src/sdr/
  schemas.py                    typed domain model
  research.py qualify.py        the researcher + qualifier (deterministic)
  write.py review.py            the writer + the no-fabrication reviewer
  agents_crew.py                the real CrewAI crew (guarded)
  crew.py                       the flow + the approval gates
  evals.py                      qualification accuracy + safety gates
  app.py store.py cli.py        API, in-memory store, CLI
  data/accounts.jsonl           labelled accounts (ICP tiers)
  tests/                        30 tests (incl. the fabrication + send gates)
frontend/                       Next.js console (accounts, campaign, approve/reject)
```

## Local workflow

```bash
make install && make web
make ci                 # ruff + pytest + eval/safety gate
make serve && make dev  # API on :8000, console on :3000
```

## Scope / ethics

Accounts and signals are synthetic. The crew never actually sends anything; "approve" records the
human decision. The point is grounded drafts and a hard human gate, not automated spam.
