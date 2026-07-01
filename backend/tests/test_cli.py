from __future__ import annotations

from sdr.cli import main


def test_eval_command_passes():
    assert main(["eval"]) == 0


def test_accounts_command():
    assert main(["accounts"]) == 0


def test_run_command():
    assert main(["run", "--id", "acc-1"]) == 0


def test_run_unknown():
    assert main(["run", "--id", "nope"]) == 1


def test_demo_command():
    assert main(["demo"]) == 0
