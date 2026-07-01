"""Observability — a guarded Langfuse v4 mirror; a no-op without keys."""

from __future__ import annotations

import os
from typing import Any

from sdr.schemas import Campaign


def _init_langfuse() -> Any | None:
    if not (os.environ.get("LANGFUSE_PUBLIC_KEY") and os.environ.get("LANGFUSE_SECRET_KEY")):
        return None
    try:  # pragma: no cover - requires keys
        from langfuse import Langfuse

        return Langfuse()
    except Exception:
        return None


class Tracer:
    def __init__(self, enabled: bool = True) -> None:
        self._client = _init_langfuse() if enabled else None

    @property
    def active(self) -> bool:
        return self._client is not None

    def record(self, campaign: Campaign) -> None:  # pragma: no cover - requires keys
        if self._client is None:
            return
        try:
            with self._client.start_as_current_span(name=f"campaign:{campaign.account_id}") as span:
                span.update(metadata={"status": campaign.status.value, "tier": campaign.qualification.tier.value})
        except Exception:
            pass
