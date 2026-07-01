"""The writer — draft outreach where every account claim points at a fact.

The draft is built from grounded claims (each carrying the id of the fact that supports it) plus a
boilerplate ask. It never asserts anything about the account that the researcher did not find, which
is what lets the reviewer guarantee no fabrication.
"""

from __future__ import annotations

from sdr.schemas import Account, Claim, Fact, OutreachDraft, Qualification

_CTA = "Would you be open to a 15-minute call next week to see if it's relevant?"


def draft(account: Account, facts: list[Fact], qual: Qualification) -> OutreachDraft:
    by_field: dict[str, Fact] = {}
    for f in facts:
        by_field.setdefault(f.field, f)

    claims: list[Claim] = []
    industry = by_field.get("industry")
    if industry:
        claims.append(Claim(text=f"I've been following {account.company} and its work in {account.industry}.", fact_id=industry.id))

    signal = next((f for f in facts if f.field == "signal"), None)
    if signal:
        claims.append(Claim(text=f"Noticed that {signal.text.rstrip('.').lower()} — often a sign teams are rethinking their tooling.", fact_id=signal.id))
    else:
        size = by_field.get("employees")
        if size:
            claims.append(Claim(text=f"At around {account.employees} people, teams your size usually feel this pain acutely.", fact_id=size.id))

    tech = next((f for f in facts if f.field == "tech"), None)
    if tech:
        claims.append(Claim(text=f"Given you run {tech.text.split('uses ')[-1].rstrip('.')}, we integrate cleanly.", fact_id=tech.id))

    subject = f"A quick idea for {account.company}"
    return OutreachDraft(subject=subject, claims=claims, cta=_CTA)
