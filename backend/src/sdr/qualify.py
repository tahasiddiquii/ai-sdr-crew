"""The qualifier — score an account against the ICP and assign a tier.

Deterministic and explainable: industry fit is the gate, then size, region, and buying signals add to
a 0-100 score that maps to a tier. An account outside the target industries is disqualified, not
force-fit, so the crew never wastes outreach (or a human's time) on a bad lead.
"""

from __future__ import annotations

from sdr.config import Settings
from sdr.schemas import Account, Fact, Qualification, Tier

_BUYING_SIGNALS = ("hiring engineers", "raised series", "scaling", "migrating to cloud", "expanding", "new cto", "new vp engineering")
_MODERN_TECH = {"kubernetes", "snowflake", "databricks", "kafka", "terraform", "airflow", "dbt"}


def qualify(account: Account, facts: list[Fact], settings: Settings) -> Qualification:
    reasons: list[str] = []
    if account.industry.lower() not in settings.industries():
        return Qualification(fit_score=0, tier=Tier.DISQUALIFIED, reasons=[f"industry '{account.industry}' is outside the ICP"])

    score = 40
    reasons.append(f"industry '{account.industry}' matches the ICP")

    if settings.icp_min_employees <= account.employees <= settings.icp_max_employees:
        score += 25
        reasons.append(f"{account.employees} employees is in the target range")
    elif account.employees < settings.icp_min_employees:
        score += 5
        reasons.append(f"{account.employees} employees is below the target range")
    else:
        score += 10
        reasons.append(f"{account.employees} employees is above the target range")

    if account.region.lower() in settings.regions():
        score += 15
        reasons.append(f"region '{account.region}' is in target")

    signal_pts = 0
    for s in account.signals:
        if any(k in s.lower() for k in _BUYING_SIGNALS):
            signal_pts += 7
            reasons.append(f"buying signal: {s}")
    tech_pts = sum(4 for t in account.tech_stack if t.lower() in _MODERN_TECH)
    score += min(20, signal_pts + tech_pts)

    score = min(100, score)
    if score >= settings.tier_a:
        tier = Tier.A
    elif score >= settings.tier_b:
        tier = Tier.B
    elif score >= settings.tier_c:
        tier = Tier.C
    else:
        tier = Tier.DISQUALIFIED
    return Qualification(fit_score=score, tier=tier, reasons=reasons)
