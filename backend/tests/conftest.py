from __future__ import annotations

import pytest

from sdr.config import reset_settings
from sdr.store import reset_store


@pytest.fixture(autouse=True)
def _isolate():
    reset_settings()
    reset_store()
    yield
    reset_settings()
    reset_store()
