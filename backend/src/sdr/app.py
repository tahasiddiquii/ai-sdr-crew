"""FastAPI backend for the SDR crew.

List accounts, run the crew (research + qualify + draft + review), fetch a campaign, and approve or
reject the outreach. Approval is the send gate: a rep must sign off, and a draft with any ungrounded
claim is refused.
"""

from __future__ import annotations

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sdr.config import get_settings
from sdr.crew import UngroundedError
from sdr.schemas import Account, Approval
from sdr.store import Store, get_store

app = FastAPI(title="ai-sdr-crew", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[get_settings().web_origin, "http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

_REP_ROLES = {"rep", "manager", "admin"}


def require_rep(x_role: str = Header(default="viewer")) -> str:
    if x_role not in _REP_ROLES:
        raise HTTPException(status_code=403, detail=f"role '{x_role}' may not approve outreach")
    return x_role


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "provider": get_settings().provider}


@app.get("/accounts")
def list_accounts(store: Store = Depends(get_store)) -> list[Account]:
    return list(store.accounts.values())


@app.post("/run/{account_id}")
def run(account_id: str, store: Store = Depends(get_store)) -> dict:
    if account_id not in store.accounts:
        raise HTTPException(status_code=404, detail="unknown account")
    return store.run(account_id).model_dump(mode="json")


@app.get("/campaign/{account_id}")
def get_campaign(account_id: str, store: Store = Depends(get_store)) -> dict:
    campaign = store.get(account_id)
    if campaign is None:
        raise HTTPException(status_code=404, detail="not run yet")
    return campaign.model_dump(mode="json")


@app.post("/campaign/{account_id}/approve")
def approve(account_id: str, decision: Approval, role: str = Depends(require_rep), store: Store = Depends(get_store)) -> dict:
    try:
        return store.approve(account_id, decision).model_dump(mode="json")
    except KeyError:
        raise HTTPException(status_code=404, detail="run the crew on this account first") from None
    except UngroundedError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from None
