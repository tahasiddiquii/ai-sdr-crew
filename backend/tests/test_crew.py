from __future__ import annotations

import pytest

from sdr.crew import Crew, UngroundedError
from sdr.data import load_accounts
from sdr.schemas import Approval, CampaignStatus, Claim, Tier


def _account(aid: str):
    return next(a for a in load_accounts() if a.id == aid)


def test_qualified_account_gets_a_draft_awaiting_approval():
    campaign = Crew().run(_account("acc-1"))
    assert campaign.status is CampaignStatus.AWAITING_APPROVAL
    assert campaign.draft is not None and campaign.needs_review


def test_disqualified_account_gets_no_outreach():
    campaign = Crew().run(_account("acc-13"))  # agriculture -> out of ICP
    assert campaign.qualification.tier is Tier.DISQUALIFIED
    assert campaign.status is CampaignStatus.DISQUALIFIED
    assert campaign.draft is None


def test_run_never_auto_approves():
    for account in load_accounts():
        assert Crew().run(account).status is not CampaignStatus.APPROVED


def test_approve_sends_grounded_outreach():
    crew = Crew()
    campaign = crew.run(_account("acc-2"))
    approved = crew.approve(campaign, Approval(approver="rep:taha", approve=True))
    assert approved.status is CampaignStatus.APPROVED


def test_reject():
    crew = Crew()
    campaign = crew.run(_account("acc-2"))
    rejected = crew.approve(campaign, Approval(approver="rep:taha", approve=False))
    assert rejected.status is CampaignStatus.REJECTED


def test_cannot_approve_ungrounded_outreach():
    crew = Crew()
    campaign = crew.run(_account("acc-2"))
    campaign.draft.claims.append(Claim(text="You are our biggest customer.", fact_id=None))
    from sdr.review import review

    campaign.review = review(campaign.draft, campaign.facts)
    with pytest.raises(UngroundedError):
        crew.approve(campaign, Approval(approver="rep:taha", approve=True))
