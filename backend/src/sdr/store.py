"""In-memory store for the API — indexes accounts and drives the crew."""

from __future__ import annotations

from sdr.config import Settings, get_settings
from sdr.crew import Crew
from sdr.data import load_accounts
from sdr.schemas import Account, Approval, Campaign


class Store:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.crew = Crew(self.settings)
        self.accounts: dict[str, Account] = {a.id: a for a in load_accounts()}
        self.campaigns: dict[str, Campaign] = {}

    def run(self, account_id: str) -> Campaign:
        campaign = self.crew.run(self.accounts[account_id])
        self.campaigns[account_id] = campaign
        return campaign

    def get(self, account_id: str) -> Campaign | None:
        return self.campaigns.get(account_id)

    def approve(self, account_id: str, approval: Approval) -> Campaign:
        if account_id not in self.campaigns:
            raise KeyError(account_id)
        return self.crew.approve(self.campaigns[account_id], approval)


_STORE: Store | None = None


def get_store() -> Store:
    global _STORE
    if _STORE is None:
        _STORE = Store()
    return _STORE


def reset_store() -> None:
    global _STORE
    _STORE = None
