---
name: ccf-integrity-auditor
description: "Audit existing CCF claims, numbers, terminology, and citations against supplied or verified evidence. Use for 引用核验, claim审计, 数字一致性, and BibTeX/context checks. Full scientific review belongs to ccf-paper-reviewer; new literature discovery belongs to ccf-literature-searcher."
metadata:
  ccf_skill_controls:
    handoff_question_mode: partial
    respect_session_denylists: true
    protect_idea_scope_in_writing: true
    private_material_safety: moderate
    shared_controls: ../ccf-common/references/
---

# CCF Integrity Auditor

## Family File Contract

Before file work, reuse canonical paths and one task/artifact working directory; default to project-root `ccfa-workfiles/<purpose>/<artifact-id>/`. Update in place, preserve inputs, and use UTF-8 with Chinese-text checks. Apply [artifact-contracts.md](../ccf-common/references/artifact-contracts.md) for naming, ownership, and task-created cleanup; handoffs inherit these paths.

## Collaboration Contract

Before specialist execution, read and apply [ccf-humanization](../ccf-humanization/SKILL.md) first, then [ccf-common](../ccf-common/SKILL.md). At every handoff, reuse their applicable active rules or refresh missing/changed ones. Both preflights are required even without prose; detailed editing, experiment, and maintenance modes run only when relevant.

Integrate necessary specialist contributions under one owner; reuse valid prerequisites and verify affected results. Follow the [cooperation routes](../ccf-common/references/routing.md) without duplicate reports.

## Core Rule

Trace each important claim to supplied evidence, each number to supplied results, and each citation to a real cited work and a supported citation context. Mark unsupported items instead of repairing them by invention.

## Modes

- `claim-audit`: claim-support and result-to-claim consistency.
- `numeric-audit`: numbers, units, table/figure/text agreement, deltas, and metric direction.
- `citation-audit`: already cited papers, BibTeX metadata, duplicate keys, DOI/arXiv/venue sanity, and citation-context support.
- `full`: all integrity checks.

Result-to-claim gate: when experiment results are about to become claims (before drafting consumes them), apply [result-to-claim-gate.md](references/result-to-claim-gate.md): run `scripts/evidence_check.py` as the deterministic evidence pre-check, then obtain an independent cross-model support judgment and route each claim as yes / partial / no, with `no` recorded as a first-class outcome.

Reference metadata verification: when the question is whether bibliography entries are transcribed correctly (authors, year, volume, pages, DOI), apply [ref-metadata-verification.md](references/ref-metadata-verification.md) — field-level comparison against publisher records with Critical/Warning/Info severities and a per-item Verified / Check suggested / Needs fix / Unverifiable label. This is distinct from citation-audit's context-support check, which judges whether a source supports the claim that cites it.

## Workflow

1. Identify supplied manuscript, figures/tables/results, bibliography, `ccfa.yaml`, and requested audit mode.
2. For claim or full audits, map the relevant claims to evidence and mark each as supported, partially supported, unsupported, overstated, or unclear. Numeric and citation audits track their scoped values or citations; add claim rows only when needed to resolve a finding.
   For a consequential result-to-claim or a contested mechanistic claim, use the [claim-promotion gate](../ccf-common/references/claim-promotion-gate.md). Keep theorem/proof status distinct from empirical evidence status, and report the strongest supported wording plus the unresolved discriminator. Reuse existing claim/evidence locations; do not create a claim database for an ordinary edit.
3. Cross-check the reported values within the requested scope across text, tables, figures, captions, abstracts, and conclusions. Use deterministic arithmetic for deltas, units, metric direction, and rounding. Distinguish not comparable from inconsistent.
   For reported ML comparisons with material statistical or mechanism claims, use the relevant [research-rigor gates](../ccf-common/references/research-rigor-gates.md): reconstruct fold/seed aggregation before nonlinear metrics, check paired sample identities and changing conditional denominators, verify declared multiplicity families when significance is claimed, and trace group-constant reward factors through normalization before accepting gradient-effect claims. Do not create new numeric evidence while auditing.
4. For citation audit, verify the identity and context support of existing citations through primary sources; metadata existence alone does not establish support. Batch independent identifiers when possible and request only identity fields before reading the source passages needed for claim support. Reuse verified source versions and anchors; refresh affected findings when a citation, claim, or source version changes. Seek new literature only when requested; broad discovery belongs to `ccf-literature-searcher`.
   For a bounded mechanical pre-check of a whole bibliography, run `scripts/format-checker.py` (offline format and tex↔bib consistency) and `scripts/verify-citations.py` (Crossref/arXiv/Semantic Scholar existence and metadata agreement) under [citation-verification-rules.md](references/citation-verification-rules.md). Their scores are pre-check grading only, never a pass verdict, and an entry whose lookups could not reach an API is reported `skipped`, not failed; per-item verification against original sources remains the audit standard.
5. For any questionable citation, separate metadata problems from context-support problems.
6. Hand off to `ccf-paper-reviewer` for full scientific judgment and to `ccf-paper-writer` for safe wording edits.
7. If the numbers and claims are consistent but the figure/table layout, caption placement, palette, float order, or rendered readability is weak, hand off to `ccf-visual-composer`.

## Output Contract

Include the fields relevant to the requested audit, with source locations and unresolved coverage. A bounded helper returns its findings to the owner without a separate full report.

```text
Mode:
Artifacts checked:
Claim-evidence matrix:
Numeric consistency findings:
Citation metadata findings:
Citation-context findings:
Severity:
Safe edit suggestions:
Next CCFA owner:
Unverified scope:
```

## Execution Boundaries

Follow `../ccf-common/references/handoff-modes.md`, `../ccf-common/references/task-modes.md`, and `../ccf-common/references/privacy-and-evidence.md`. Finish the checkable portions when an attachment or source is missing. Report exact file/page/table locations, affected values or claims, evidence, and severity; mark unverified coverage separately from failures. An audit request does not authorize manuscript rewriting. Use existing authorization for explicitly requested fixes and preserve raw measurements.
