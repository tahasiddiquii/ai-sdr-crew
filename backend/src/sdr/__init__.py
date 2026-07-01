"""ai-sdr-crew — a sales-development crew that qualifies leads and drafts grounded outreach.

A researcher, qualifier, writer, and reviewer (CrewAI) collaborate to research an account, qualify it
against an ICP, and draft outreach whose every claim is grounded in a fact. Nothing is sent without a
human. Runs fully offline with a deterministic crew; ``SDR_PROVIDER=openai`` switches to real agents.
"""

from __future__ import annotations

from sdr.config import Settings, get_settings
from sdr.crew import Crew, UngroundedError
from sdr.data import load_accounts, load_labelled
from sdr.evals import evaluate
from sdr.schemas import Account, Approval, Campaign, CampaignStatus, Qualification, Tier

__version__ = "0.1.0"

__all__ = [
    "Account",
    "Approval",
    "Campaign",
    "CampaignStatus",
    "Crew",
    "Qualification",
    "Settings",
    "Tier",
    "UngroundedError",
    "evaluate",
    "get_settings",
    "load_accounts",
    "load_labelled",
    "__version__",
]
