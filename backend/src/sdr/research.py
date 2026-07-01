"""The researcher — turn an account into a set of citable facts.

In production this fans out to enrichment APIs and the web; here it derives facts deterministically
from the seeded account record, so every downstream claim can point at a real fact id.
"""

from __future__ import annotations

from sdr.schemas import Account, Fact


def research(account: Account) -> list[Fact]:
    facts = [
        Fact(id=f"{account.id}-industry", field="industry", text=f"{account.company} operates in {account.industry}."),
        Fact(id=f"{account.id}-size", field="employees", text=f"{account.company} has roughly {account.employees} employees."),
        Fact(id=f"{account.id}-region", field="region", text=f"{account.company} is based in {account.region}."),
    ]
    for i, signal in enumerate(account.signals):
        facts.append(Fact(id=f"{account.id}-signal{i}", field="signal", text=signal))
    for tech in account.tech_stack:
        facts.append(Fact(id=f"{account.id}-tech-{tech.lower()}", field="tech", text=f"{account.company} uses {tech}."))
    return facts
