"""Real crew — CrewAI, activated only when a cloud provider is set.

The offline default never imports this. A small crew (writer + reviewer) drafts the outreach; the
returned draft goes through the *same* deterministic grounding review, so the no-fabrication guarantee
holds whichever writer produced it.
"""

from __future__ import annotations

from sdr.config import Settings
from sdr.schemas import Account, Claim, Fact, OutreachDraft, Qualification


def draft_with_crew(account: Account, facts: list[Fact], qual: Qualification, settings: Settings) -> OutreachDraft:  # pragma: no cover - requires keys
    from crewai import Agent, Crew, Process, Task

    fact_block = "\n".join(f"- [{f.id}] {f.text}" for f in facts)
    writer = Agent(
        role="SDR copywriter",
        goal="Write a short, specific outreach email grounded only in the provided facts.",
        backstory="You never invent facts about a company. Every claim cites a fact id.",
        llm=f"{settings.provider}/{settings.model}",
    )
    task = Task(
        description=(
            f"Company: {account.company} (tier {qual.tier.value}).\nFacts:\n{fact_block}\n\n"
            "Write 2-3 sentences of outreach. Each sentence must be supported by a fact above; "
            "prefix each with the [fact_id] it uses. End with a soft call to action."
        ),
        expected_output="Lines of 'text' each prefixed by [fact_id], then one CTA line.",
        agent=writer,
    )
    output = str(Crew(agents=[writer], tasks=[task], process=Process.sequential).kickoff())
    return _parse(output, account, facts)


def _parse(output: str, account: Account, facts: list[Fact]) -> OutreachDraft:  # pragma: no cover - requires keys
    fact_ids = {f.id for f in facts}
    claims: list[Claim] = []
    cta = ""
    for line in output.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith("[") and "]" in line:
            fid, _, text = line[1:].partition("]")
            fid = fid.strip()
            claims.append(Claim(text=text.strip(), fact_id=fid if fid in fact_ids else None))
        else:
            cta = line
    return OutreachDraft(subject=f"A quick idea for {account.company}", claims=claims, cta=cta)
