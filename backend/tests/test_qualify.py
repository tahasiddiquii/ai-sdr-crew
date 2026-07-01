from __future__ import annotations

from sdr.config import get_settings
from sdr.qualify import qualify
from sdr.research import research
from sdr.schemas import Account, Tier


def _q(account: Account):
    return qualify(account, research(account), get_settings())


def test_strong_fit_is_tier_a():
    account = Account(id="x", company="X", industry="saas", employees=400, region="north america",
                      tech_stack=["Kubernetes", "Snowflake"], signals=["hiring engineers", "raised Series B"])
    q = _q(account)
    assert q.tier is Tier.A and q.fit_score >= 80


def test_out_of_icp_industry_is_disqualified():
    account = Account(id="x", company="X", industry="agriculture", employees=500, region="north america")
    q = _q(account)
    assert q.tier is Tier.DISQUALIFIED and q.fit_score == 0


def test_wrong_region_and_no_signals_lowers_tier():
    account = Account(id="x", company="X", industry="saas", employees=3000, region="asia", tech_stack=["Kubernetes"])
    q = _q(account)
    assert q.tier is Tier.B  # in-industry + size, but no region/signals


def test_reasons_are_explained():
    account = Account(id="x", company="X", industry="fintech", employees=1200, region="europe")
    q = _q(account)
    assert any("industry" in r for r in q.reasons)
