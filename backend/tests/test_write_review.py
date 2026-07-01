from __future__ import annotations

from sdr.config import get_settings
from sdr.qualify import qualify
from sdr.research import research
from sdr.review import review
from sdr.schemas import Account, Claim
from sdr.write import draft


def _account() -> Account:
    return Account(id="x", company="Acme", industry="saas", employees=400, region="north america",
                   tech_stack=["Kubernetes"], signals=["hiring engineers"])


def test_every_written_claim_is_grounded():
    account = _account()
    facts = research(account)
    outreach = draft(account, facts, qualify(account, facts, get_settings()))
    result = review(outreach, facts)
    assert result.grounded
    assert all(c.fact_id for c in outreach.claims)


def test_reviewer_flags_a_fabricated_claim():
    account = _account()
    facts = research(account)
    outreach = draft(account, facts, qualify(account, facts, get_settings()))
    outreach.claims.append(Claim(text="You just raised a $100M round.", fact_id=None))
    result = review(outreach, facts)
    assert not result.grounded and result.ungrounded_claims


def test_reviewer_flags_a_claim_citing_an_unknown_fact():
    account = _account()
    facts = research(account)
    outreach = draft(account, facts, qualify(account, facts, get_settings()))
    outreach.claims.append(Claim(text="You use Widget.", fact_id="not-a-real-fact"))
    assert not review(outreach, facts).grounded
