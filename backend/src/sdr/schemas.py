"""Typed domain model for the SDR crew.

An account is researched into facts, qualified against an ICP into a tier, and (if it qualifies)
turned into an outreach draft whose every claim is grounded in a fact. A reviewer checks that
grounding, and nothing is sent without human approval.
"""

from __future__ import annotations

from datetime import UTC, datetime
from enum import Enum

from pydantic import BaseModel, Field


def _now() -> datetime:
    return datetime.now(UTC)


class Tier(str, Enum):
    A = "A"
    B = "B"
    C = "C"
    DISQUALIFIED = "disqualified"


class CampaignStatus(str, Enum):
    DISQUALIFIED = "disqualified"
    AWAITING_APPROVAL = "awaiting_approval"
    APPROVED = "approved"
    REJECTED = "rejected"


class Account(BaseModel):
    id: str
    company: str
    industry: str
    employees: int
    region: str
    tech_stack: list[str] = Field(default_factory=list)
    signals: list[str] = Field(default_factory=list)  # e.g. "hiring engineers", "raised Series B"


class Fact(BaseModel):
    id: str
    field: str
    text: str


class Qualification(BaseModel):
    fit_score: int = Field(ge=0, le=100)
    tier: Tier
    reasons: list[str] = Field(default_factory=list)


class Claim(BaseModel):
    text: str
    fact_id: str | None = None  # the fact that grounds this claim; None means fabricated


class OutreachDraft(BaseModel):
    subject: str
    claims: list[Claim] = Field(default_factory=list)  # statements about the account, each grounded
    cta: str = ""  # boilerplate ask; not a factual claim about the account

    def body(self) -> str:
        return " ".join(c.text for c in self.claims) + (f" {self.cta}" if self.cta else "")


class ReviewResult(BaseModel):
    grounded: bool = True
    ungrounded_claims: list[str] = Field(default_factory=list)
    note: str = ""


class Approval(BaseModel):
    approver: str
    approve: bool
    note: str = ""
    at: datetime = Field(default_factory=_now)


class Step(BaseModel):
    agent: str  # researcher | qualifier | writer | reviewer
    detail: str


class Trace(BaseModel):
    provider: str = "mock"
    model: str = "mock"
    steps: list[Step] = Field(default_factory=list)
    tokens_in: int = 0
    tokens_out: int = 0
    cost_usd: float = 0.0


class Campaign(BaseModel):
    account_id: str
    company: str
    status: CampaignStatus
    qualification: Qualification
    facts: list[Fact] = Field(default_factory=list)
    draft: OutreachDraft | None = None
    review: ReviewResult | None = None
    needs_review: bool = False
    approval: Approval | None = None
    trace: Trace = Field(default_factory=Trace)
    created_at: datetime = Field(default_factory=_now)
