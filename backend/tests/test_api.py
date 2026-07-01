from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from sdr.app import app
from sdr.store import reset_store


@pytest.fixture(autouse=True)
def _fresh():
    reset_store()
    yield
    reset_store()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


def test_health(client: TestClient):
    assert client.get("/health").json()["provider"] == "mock"


def test_accounts_listed(client: TestClient):
    r = client.get("/accounts")
    assert r.status_code == 200 and len(r.json()) == 16


def test_run_qualified_account(client: TestClient):
    body = client.post("/run/acc-1").json()
    assert body["status"] == "awaiting_approval"
    assert body["qualification"]["tier"] == "A"


def test_viewer_cannot_approve(client: TestClient):
    client.post("/run/acc-1")
    r = client.post("/campaign/acc-1/approve", json={"approver": "viewer:x", "approve": True}, headers={"X-Role": "viewer"})
    assert r.status_code == 403


def test_rep_approves(client: TestClient):
    client.post("/run/acc-1")
    r = client.post("/campaign/acc-1/approve", json={"approver": "rep:taha", "approve": True}, headers={"X-Role": "rep"})
    assert r.status_code == 200 and r.json()["status"] == "approved"


def test_approve_before_run_is_404(client: TestClient):
    r = client.post("/campaign/acc-2/approve", json={"approver": "rep:x", "approve": True}, headers={"X-Role": "rep"})
    assert r.status_code == 404
