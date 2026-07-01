---
name: ai-sdr
description: >
  Qualify a sales account against an ICP and, if it fits, draft outreach where every claim about the
  account is grounded in a researched fact. Disqualify off-ICP accounts instead of force-fitting them,
  and never send without human approval. Use when triaging accounts and drafting first-touch outreach.
---

# AI SDR skill

A portable contract for the crew that turns an account into qualified, grounded outreach. The
implementation lives in `backend/src/sdr/`; the contract below is what keeps it honest and safe.

## The crew (a flow of four agents)

```
researcher -> qualifier -> (stop if disqualified) -> writer -> reviewer -> await human approval
```

## Research

Turn the account into a set of citable facts, each with an id. Every later claim must point at one.

## Qualify

Score the account against the ICP: industry fit is the gate, then size, region, and buying signals add
to a 0-100 score that maps to a tier (A/B/C). Off-ICP -> disqualified, with reasons. Do not force-fit.

## Write

Draft 2-3 sentences. Each sentence that asserts something about the account is a claim carrying the id
of the fact that supports it. Boilerplate (the ask) is not a claim.

## Review (the no-fabrication gate)

Every claim must point at a real fact. A claim with no fact, or one citing a fact not in the account's
set, is ungrounded. A draft with any ungrounded claim cannot be approved for sending.

## Approve (the send gate)

Nothing is sent without a human. Approval requires a rep, and ungrounded outreach is refused even to a
rep until it is fixed.

## Invocation

```bash
sdr run --id acc-1     # research, qualify, draft, review
sdr eval               # qualification accuracy + no-fabrication / no-auto-send gates
```

```python
from sdr import Crew, load_accounts
campaign = Crew().run(load_accounts()[0])
campaign.qualification.tier, campaign.draft, campaign.review.grounded
```
