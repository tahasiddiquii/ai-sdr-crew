"""Command line for the SDR crew.

    sdr accounts               the target accounts
    sdr run --id acc-1          research, qualify, and (if a fit) draft outreach
    sdr eval                    qualification accuracy + no-fabrication / no-auto-send gates
    sdr demo                    a narrated run, including the ungrounded-claim block
    sdr serve                   run the FastAPI backend
"""

from __future__ import annotations

import argparse
import sys

from rich.console import Console
from rich.table import Table

from sdr.crew import Crew, UngroundedError
from sdr.data import load_accounts
from sdr.evals import evaluate, write_markdown
from sdr.schemas import Approval, Claim, Tier

console = Console()

_TIER_STYLE = {"A": "bold green", "B": "green", "C": "yellow", "disqualified": "dim"}


def _render(campaign) -> None:
    q = campaign.qualification
    console.print(f"[bold]{campaign.company}[/bold]  tier=[{_TIER_STYLE[q.tier.value]}]{q.tier.value}[/]  "
                  f"fit={q.fit_score}/100  status=[cyan]{campaign.status.value}[/cyan]")
    for r in q.reasons:
        console.print(f"  · {r}")
    if campaign.draft:
        console.print(f"\n[bold]Subject:[/bold] {campaign.draft.subject}")
        console.print(campaign.draft.body())
        console.print(f"[dim]review: {campaign.review.note}[/dim]")


def _run(args: argparse.Namespace) -> int:
    accounts = {a.id: a for a in load_accounts()}
    if args.id not in accounts:
        console.print(f"[red]no account {args.id}[/red]")
        return 1
    _render(Crew().run(accounts[args.id]))
    return 0


def _accounts(_args: argparse.Namespace) -> int:
    table = Table(header_style="bold cyan")
    for col in ("id", "company", "industry", "employees", "region"):
        table.add_column(col)
    for a in load_accounts():
        table.add_row(a.id, a.company, a.industry, str(a.employees), a.region)
    console.print(table)
    return 0


def _eval(args: argparse.Namespace) -> int:
    report = evaluate()
    console.print(f"[bold]qualification accuracy[/bold] {report.qualification_accuracy:.3f}  "
                  f"dq-recall {report.dq_recall:.3f}  drafts {report.drafted}")
    console.print(f"no-fabrication — ungrounded claims: [bold]{report.ungrounded_claims}[/bold]  "
                  f"send-gate — auto-approved: [bold]{report.auto_approved}[/bold]")
    if args.report:
        from pathlib import Path

        path = Path(args.report)
        path.parent.mkdir(parents=True, exist_ok=True)
        write_markdown(report, path)
        console.print(f"[green]wrote[/green] {path}")
    if report.passed():
        console.print("[bold green]GATE PASSED[/bold green]")
        return 0
    console.print(f"[bold red]GATE FAILED[/bold red] — {'; '.join(report.failures)}")
    return 1


def _demo(_args: argparse.Namespace) -> int:
    console.rule("[bold]ai-sdr-crew")
    crew = Crew()
    accounts = {a.id: a for a in load_accounts()}

    fit = next(a for a in accounts.values() if crew.run(a).qualification.tier in (Tier.A, Tier.B))
    campaign = crew.run(fit)
    _render(campaign)

    console.print("\n[dim]# a fabricated claim is refused at send time[/dim]")
    campaign.draft.claims.append(Claim(text="You just closed a $50M round.", fact_id=None))
    from sdr.review import review as review_draft

    campaign.review = review_draft(campaign.draft, campaign.facts)
    try:
        crew.approve(campaign, Approval(approver="rep:taha", approve=True))
        console.print("[red]sent (should never print)[/red]")
    except UngroundedError as exc:
        console.print(f"[green]blocked[/green]: {exc}")

    console.print()
    return _eval(argparse.Namespace(report=None))


def _serve(args: argparse.Namespace) -> int:
    import uvicorn

    uvicorn.run("sdr.app:app", host=args.host, port=args.port, reload=args.reload)
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="sdr", description="AI SDR crew")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("accounts", help="list target accounts").set_defaults(func=_accounts)

    p_run = sub.add_parser("run", help="run the crew on one account")
    p_run.add_argument("--id", required=True)
    p_run.set_defaults(func=_run)

    p_eval = sub.add_parser("eval", help="qualification + safety gates")
    p_eval.add_argument("--report")
    p_eval.set_defaults(func=_eval)

    sub.add_parser("demo", help="narrated run with the fabrication block").set_defaults(func=_demo)

    p_serve = sub.add_parser("serve", help="run the FastAPI backend")
    p_serve.add_argument("--host", default="127.0.0.1")
    p_serve.add_argument("--port", type=int, default=8000)
    p_serve.add_argument("--reload", action="store_true")
    p_serve.set_defaults(func=_serve)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
