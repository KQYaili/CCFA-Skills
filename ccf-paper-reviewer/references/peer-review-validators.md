# Peer-Review Local Validators

Four deterministic, local-only validators that gate the mechanical side of
a review assignment. They check structure, authorization, and internal
consistency — none of them judges scientific quality, and all run offline
on local files (JSON / CSV / Markdown) with no network access.

| Script | Input | What it enforces |
| --- | --- | --- |
| `scripts/validate_review_intake.py` | Completed intake JSON | Scope, authorization, and conflict hard gate (below) |
| `scripts/validate_claim_evidence.py` | Claim–evidence matrix CSV | Every claim row carries an evidence pointer and a support status; unmapped claims fail |
| `scripts/audit_statistics_reproducibility.py` | Methods/statistics checklist JSON | Statistical reporting completeness, including the equivalence rule (below) and reproducibility fields |
| `scripts/lint_review.py` | Draft review Markdown | Tone, channel separation (comments to authors vs confidential editor channel), and actionability of the review text |

All four share `scripts/_common.py`. Each prints a structured report and
exits non-zero on hard failures.

## The Intake Hard Gate

The intake validator treats conflicts as an authorization question, not a
disclosure formality:

- A conflict marked `disclosed_to_editor` **remains blocked**. Disclosure
  informs the editor; it does not clear the reviewer.
- A conflict is cleared only by an actual `editor_cleared` state, or by
  `none_identified` when no conflict exists.
- Unassessed or unresolved conflicts block the review from proceeding.
- Never mark a conflict cleared merely to make the validator pass — the
  gate exists precisely to make that shortcut visible.

## The Equivalence Rule (statistics audit)

A non-significant difference test does **not** establish equivalence. A
claim of equivalence or non-inferiority is supported only by an explicit
equivalence test (e.g. TOST against a pre-stated margin) or a
non-inferiority analysis; the audit flags equivalence wording backed only
by "p > 0.05" as unsupported. This mirrors the claim-promotion gate's rule
that a null result is preserved as a null, never rewritten as equivalence.

## Use

Run the intake validator before accepting an assignment's materials, the
claim–evidence validator when a review (or a rebuttal response) asserts a
claim–evidence mapping, the statistics audit alongside a scientific review
of an empirical paper, and the lint on the near-final review text. Their
outputs are inputs to the review, recorded like other mechanical
pre-checks; a pass certifies form and authorization, not correctness.

> Provenance: adapted from K-Dense-AI/scientific-agent-skills (MIT License,
> Copyright (c) 2025 K-Dense Inc.), `skills/peer-review/scripts/`,
> batch-2 integration 2026-11-03. The four validators and their shared
> `_common.py` are imported with logic unchanged. The upstream skill's
> self-citation clause (in its SKILL.md prose) was **not** imported, and no
> part of this suite requires or requests citing the source toolkit.
> Upstream pieces not imported: `audit_citations.py` (citation existence
> machinery already lives with `ccf-integrity-auditor`),
> `generate_review_scaffold.py`, and `select_reporting_guidelines.py`
> (biomedical reporting-guideline selection, out of this repo's scope).
