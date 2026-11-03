# Three-Blind Review: The Multi-Review Mode

Use when a consequential manuscript warrants more than one independent
scientific review and the value lies in *genuine* independence: three
mutually blind reports, frozen before any comparison, followed by a
separate forensic pass and a synthesis that never rewrites the reports.
This is the multi-review mode of this skill; the single-pass workflow in
[review-workflow.md](review-workflow.md) remains the default for ordinary
requests.

## Protocol

1. **Isolate.** Run each of the three reviewers in a genuinely separate
   context (separate subagent, process, or invocation), with the manuscript
   and the review charge only — no other reviewer's text, no shared concern
   ledger, no main-review conclusions. If the environment cannot isolate
   contexts, produce one report per invocation or state explicitly that
   mutual blindness cannot be guaranteed; never present shared-context
   drafting as independent review.
2. **Review independently.** Each reviewer assesses the paper on its own
   and builds its own concern ledger. Every substantive concern carries:
   a **stable ID** (reviewer-local, e.g. `R1-M1` for reviewer 1's first
   major concern), a faithful `claim_pointer` (the manuscript claim it
   targets), and a checkable `evidence_pointer` (section, figure, table,
   or equation where the evidence lives — mark the location as missing
   instead of inventing one).
3. **Freeze.** Finalize each report before any cross-comparison. Do not
   show a completed or partial report to another reviewer, do not
   redistribute concerns to control overlap, and do not edit a report after
   freezing to reduce duplication or manufacture disagreement. Natural
   duplication and disagreement are evidence the blindness worked.
4. **Forensic consistency audit (separate editorial pass).** After all
   reports are frozen, run a deterministic consistency pass over the
   manuscript itself: arithmetic, metric bounds, aggregation levels,
   prose-vs-table ordering, duplicate displays, dispersion anomalies,
   provenance and reproducibility details. Classify findings as confirmed
   internal error / aggregation ambiguity / provenance gap / suspected
   duplication / unresolved input needed / not assessable / passed.
   **Never feed audit findings back into reviewer contexts, and never edit
   frozen reports after the audit.** The audit is not a fourth review.
5. **Synthesize last.** In a separate pass, reconcile the frozen reports'
   local IDs to shared synthesis keys. A concern counts as **consensus**
   only when at least two frozen reports independently raised the same
   underlying concern. Keep forensic-audit findings in their own category —
   an audit finding is not reviewer consensus unless two frozen reports
   independently raised it too.

## Output

Three frozen reports (unchanged), the forensic audit findings, and one
synthesis that preserves which concerns are single-reviewer, which are
consensus, and which came from the audit. Scores, if the venue rubric
requires them, follow [calibration-and-rank.md](calibration-and-rank.md);
the three-blind structure governs independence and evidence discipline,
not a separate scoring scale.

> Provenance: adapted from Yuan1z0825/nature-skills (Apache License 2.0),
> `skills/nature-reviewer` (SKILL.md and references/reviewer-workflow.md,
> references/forensic-consistency-audit.md), batch-2 integration
> 2026-11-03. The upstream Nature-specific editorial criteria, domain gates,
> and prose-punctuation house rules were not imported.
