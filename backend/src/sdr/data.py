"""Load the labelled account set (account record + gold ICP tier)."""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from sdr.schemas import Account


def _data_file() -> Path:
    here = Path(__file__).resolve()
    for parent in [here.parent, *here.parents]:
        candidate = parent / "data" / "accounts.jsonl"
        if candidate.exists():
            return candidate
    raise FileNotFoundError("data/accounts.jsonl not found")


@lru_cache(maxsize=1)
def _rows() -> list[dict]:
    with _data_file().open() as fh:
        return [json.loads(line) for line in fh if line.strip()]


def load_accounts() -> list[Account]:
    return [Account(**row["account"]) for row in _rows()]


def load_labelled() -> list[tuple[Account, str]]:
    return [(Account(**row["account"]), row["gold_tier"]) for row in _rows()]
