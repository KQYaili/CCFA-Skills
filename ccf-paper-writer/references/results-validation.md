# Results-As-Validation Table

Use when drafting or auditing the Results of a paper that has a
[contribution contract](contribution-contract.md). Results do not speak for
themselves: each Results unit must validate at least one contribution
promise, and the table makes that mapping explicit *before* the prose
hardens around unmapped numbers.

## The Table

One row per Results unit (subsection, table, or figure group), kept with
the manuscript's working notes as `results_validation.md`:

| Results unit | Contribution claim tested | Result / evidence | Allowed interpretation | Interpretation NOT allowed |
| --- | --- | --- | --- | --- |

- **Contribution claim tested** — the promise from the contract (C1, C2, …
  or the statement itself). A metric-only row that validates no promise is
  a hard failure: map it to a contribution or cut the unit.
- **Result / evidence** — the actual outcome and where it lives (run,
  table, figure). A claim with no result behind it is equally a hard
  failure.
- **Allowed interpretation** — the strongest honest reading of this row.
- **Interpretation NOT allowed** — the overclaim this row does not license.
  This column is the point of the exercise: it converts the contract's
  Claim Boundary into per-row wording law.

Mechanical check:

```bash
python3 scripts/results_validation_check.py <working-dir> [--json] [--write]
```

Exit 0 requires: the table exists, every data row has both a claim and
evidence, and rows are counted as mapped only when both are present. Empty
Allowed / NOT-Allowed cells are warnings, not failures — but a Results
section whose rows systematically lack the NOT-allowed column is not
finished.

## Where The Table Feeds

The completed table is a writer-side input artifact for two downstream
gates, not a gate itself:

- the [result-to-claim gate](../../ccf-integrity-auditor/references/result-to-claim-gate.md)
  consumes the claim↔evidence mapping as its claims list starting point;
- the [claim-promotion gate](../../ccf-common/references/claim-promotion-gate.md)
  consumes the Allowed / NOT-allowed columns when bounding manuscript
  wording.

Keep one table per manuscript, updated in place; do not fork it per draft.

> Provenance: adapted from WUBING2023/PaperSpine (MIT License),
> `dist/claude/skills/paper-spine/scripts/results_validation_check.py`,
> batch-2 integration 2026-11-03. The script logic is unchanged; the
> Allowed / Not-Allowed interpretation columns, optional upstream, are
> treated here as required content (warnings until filled).
