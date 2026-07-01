"""The reviewer — the no-fabrication guardrail.

Every claim in a draft must point at a fact the researcher actually found. A claim with no fact id, or
one that references a fact not in the account's set, is flagged as ungrounded. A draft with any
ungrounded claim cannot be approved for sending; a human must fix it first.
"""

from __future__ import annotations

from sdr.schemas import Fact, OutreachDraft, ReviewResult


def review(draft: OutreachDraft, facts: list[Fact]) -> ReviewResult:
    fact_ids = {f.id for f in facts}
    ungrounded = [c.text for c in draft.claims if not c.fact_id or c.fact_id not in fact_ids]
    if ungrounded:
        return ReviewResult(grounded=False, ungrounded_claims=ungrounded, note=f"{len(ungrounded)} claim(s) not grounded in a fact")
    return ReviewResult(grounded=True, note="every claim is grounded in a researched fact")
