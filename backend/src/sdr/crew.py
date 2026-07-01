"""The crew — the flow that runs the four agents and enforces the gates.

researcher -> qualifier -> (stop if disqualified) -> writer -> reviewer -> await human approval.
Two gates: a disqualified account never gets outreach, and a draft with any ungrounded claim can never
be approved for sending. In ``mock`` mode deterministic agents drive it; ``SDR_PROVIDER=openai`` swaps
in a real CrewAI crew for the writing step through the same seam.
"""

from __future__ import annotations

from sdr.config import Settings, get_settings
from sdr.qualify import qualify
from sdr.research import research
from sdr.review import review
from sdr.schemas import Account, Approval, Campaign, CampaignStatus, Step, Tier, Trace
from sdr.tracing import Tracer
from sdr.write import draft as draft_mock


class UngroundedError(RuntimeError):
    """Raised when someone tries to send outreach that contains an ungrounded claim."""


class Crew:
    def __init__(self, settings: Settings | None = None, tracer: Tracer | None = None) -> None:
        self.settings = settings or get_settings()
        self.tracer = tracer or Tracer()

    def _draft(self, account, facts, qual):
        if self.settings.provider in ("openai", "anthropic"):  # pragma: no cover - requires keys
            from sdr.agents_crew import draft_with_crew

            return draft_with_crew(account, facts, qual, self.settings)
        return draft_mock(account, facts, qual)

    def run(self, account: Account) -> Campaign:
        facts = research(account)
        qual = qualify(account, facts, self.settings)
        steps = [
            Step(agent="researcher", detail=f"gathered {len(facts)} fact(s)"),
            Step(agent="qualifier", detail=f"tier {qual.tier.value}, fit {qual.fit_score}/100"),
        ]

        if qual.tier == Tier.DISQUALIFIED:
            steps.append(Step(agent="qualifier", detail="disqualified -> no outreach"))
            return self._finish(account, CampaignStatus.DISQUALIFIED, qual, facts, None, None, False, steps)

        outreach = self._draft(account, facts, qual)
        result = review(outreach, facts)
        steps.append(Step(agent="writer", detail=f"drafted {len(outreach.claims)} grounded claim(s)"))
        steps.append(Step(agent="reviewer", detail=result.note))
        return self._finish(account, CampaignStatus.AWAITING_APPROVAL, qual, facts, outreach, result, True, steps)

    def approve(self, campaign: Campaign, approval: Approval) -> Campaign:
        if approval.approve and campaign.review is not None and not campaign.review.grounded:
            raise UngroundedError("cannot send outreach with ungrounded claims; a human must fix it first")
        campaign.approval = approval
        campaign.status = CampaignStatus.APPROVED if approval.approve else CampaignStatus.REJECTED
        self.tracer.record(campaign)
        return campaign

    def _finish(self, account, status, qual, facts, outreach, result, needs_review, steps) -> Campaign:
        tin = 150 + sum(len(f.text.split()) for f in facts)
        tout = 40 * (len(outreach.claims) if outreach else 1)
        campaign = Campaign(
            account_id=account.id, company=account.company, status=status, qualification=qual,
            facts=facts, draft=outreach, review=result, needs_review=needs_review,
            trace=Trace(provider=self.settings.provider, model=self.settings.model, steps=steps,
                        tokens_in=tin, tokens_out=tout, cost_usd=round(tin / 1e6 * 1.25 + tout / 1e6 * 10.0, 6)),
        )
        self.tracer.record(campaign)
        return campaign
