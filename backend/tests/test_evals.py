from __future__ import annotations

from sdr.evals import THRESHOLDS, evaluate


def test_gate_passes():
    report = evaluate()
    assert report.passed(), report.failures
    assert report.qualification_accuracy >= THRESHOLDS["qualification_accuracy"]


def test_no_fabrication_across_all_drafts():
    report = evaluate()
    assert report.ungrounded_claims == 0


def test_nothing_is_auto_sent():
    report = evaluate()
    assert report.auto_approved == 0


def test_bad_leads_are_screened_out():
    report = evaluate()
    assert report.dq_recall >= 0.9  # disqualified accounts are caught


def test_accuracy_is_honestly_below_one():
    report = evaluate()
    assert report.qualification_accuracy < 1.0  # a boundary case is a genuine miss


def test_write_markdown(tmp_path):
    from sdr.evals import write_markdown

    path = tmp_path / "eval.md"
    write_markdown(evaluate(), path)
    text = path.read_text()
    assert "evaluation report" in text and "No-fabrication gate" in text
