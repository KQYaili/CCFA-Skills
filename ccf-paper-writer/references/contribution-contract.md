# Contribution Contract: The Pre-Drafting Gate

Use before substantive drafting of a full paper (or a full rewrite of its
argument). **No confirmed contribution contract, no drafting.** A paper is
judged on its contribution — the one defensible thing it adds — not on
prose polish; motivation explains why a reader should care, contribution
states what the paper delivers and is willing to be judged on. The two are
not interchangeable, and this gate refuses to let motivation stand in for a
contribution.

## The Contract

Record the contract in the manuscript task's existing notes (a standalone
`confirmed_contribution.md` in the paper's working directory when the task
keeps one). Four sections, each a `| Field | Content |` table; every row
must be filled with a concrete entry — `scripts/contribution_check.py`
treats empty cells, TODO/TBD, and template placeholders as failures,
because an unfilled cell means the decision was never made.

1. **Core Contribution** — main contribution statement (one sentence, one
   claim, falsifiable); contribution type (new method / dataset / theory /
   empirical finding / system / analysis-or-benchmark / application);
   one-sentence reviewer payoff (the value to the field, not the activity
   performed).
2. **Why This Contribution Is Needed** — field problem; specific gap (the
   exact hole, not "X is understudied"); concrete challenge (why the gap is
   still open); why prior work leaves it unresolved (closest approaches,
   and the specific reason each does not close it).
3. **How This Paper Responds** — design response (the mechanism, tied to
   the challenge); evidence required (what a skeptical reviewer would
   demand — listed *before* checking what exists); evidence available;
   evidence missing. If "evidence missing" is non-empty, the core statement
   must be softened or the work done first; an honest entry here is what
   prevents over-claiming.
4. **Claim Boundary** — strong claims allowed (fully backed by evidence
   available); claims to soften or avoid; novelty risk (the most likely
   "already done by X" objection and the honest answer); significance risk
   (the most likely "so what / too narrow" objection and the honest answer).

Run the mechanical check before drafting:

```bash
python3 scripts/contribution_check.py <working-dir> [--json] [--write]
```

Exit 0 = all four sections present and substantive. The check verifies the
contract is *filled*, not that the contribution is *good* — that judgment
stays with the author and reviewers.

## Motivation Thread

Once the contract exists, it is the manuscript's spine: the Introduction
stages it as a ladder (problem → prior progress → gap + challenge → research
question → contribution promise), and every later section must trace back
to the core statement. A paragraph that neither advances, supports, nor
bounds that statement does not belong. If drafting discovers the contract
is wrong, amend the contract first and re-run the check — do not let the
prose quietly drift to a different contribution.

## Relation To Neighbouring Gates

- [argument-spine-audit.md](argument-spine-audit.md) runs **after** a draft
  exists: it reverse-outlines the draft against the promise. This contract
  runs **before** drafting and creates the promise the audit later checks
  against.
- The Claim Boundary section must agree with the
  [claim-promotion gate](../../ccf-common/references/claim-promotion-gate.md):
  wording the promotion gate has bounded or blocked may not reappear at
  full strength in the contract.
- [results-validation.md](results-validation.md) closes the loop at the
  other end: each Results unit must map back to a promise made here.

> Provenance: adapted from WUBING2023/PaperSpine (MIT License),
> `dist/claude/skills/paper-spine/references/contribution.md` and
> `scripts/contribution_check.py`, batch-2 integration 2026-11-03. The
> PaperSpine orchestrator, its self-update and telemetry behaviour, and its
> rewriting-output directory conventions were not imported; the contract
> lives in CCFA's existing manuscript notes.
