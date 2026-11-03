# Claim Promotion: Evidence To Manuscript

Use when a **material empirical result** is about to become a main paper, abstract, caption, rebuttal or public report claim, or when a review challenges its support. Work on the existing comparison and source artifacts, not a mandatory new claim database. For a simple factual answer or a purely proposed design, preserve its status without opening this gate.

## Distinguish The Two Axes

- **Formal status**: a mathematical statement may be proposed, proved under stated assumptions, refuted by a valid counterexample, or unresolved. A proof check is not an empirical replication.
- **Empirical support**: a comparison may be planned, observed on a specified dataset, support a bounded effect under a checked protocol, contradict a prior expectation, or remain unverified. A correct code path alone is not an observed outcome.

Never collapse these into a single "verified" boolean. A figure `status=verified` in the Figure Registry describes an assessed graphic, **not** proof of every scientific interpretation in the caption. Citations establishing paper identity are not automatically evidence that the cited passage supports the intended statement.

## Smallest Useful Promotion Record

For each decision-changing assertion, recover, in the existing manuscript notes, run manifest or handoff:

| Element | Required question |
| --- | --- |
| Claim and target wording | Exactly what is being asserted, under which model/task/setting? |
| Evidence locator | Which raw run, table, source passage, proof or figure **actually** contains the observation? |
| Method and comparison identity | Which code/model revision, baseline, compute budget, split, seed/fold and decision rule produced it? |
| Metric and estimand | What are the observation unit, denominator, aggregation order, uncertainty and sample size, if relevant? |
| Competing explanation | Could selection, reuse of test data, baseline budget, normalization, evaluator drift or missing trials explain it? |
| Bounded wording | What sentence is supported? What stronger wording must **not** be used? |
| Status/next action | Supported within scope, descriptive only, unresolved, contradicted, or requires a specific further check? |

A source path or a passing structural test certifies neither the underlying measurement nor its interpretation. Recompute a consequential displayed number from available source data when possible; inspect the actual experimental result before asserting a mechanistic effect. Record an inaccessible source or missing run as **unverified**, not as a valid zero or completed run.

## Promotion Decisions

- **Supported within scope**: protocol, execution identity, measurement and declared comparison are reconciled; allow explicit, scoped wording with uncertainty and relevant limits.
- **Descriptive / exploratory**: a real observation but not an independent confirmatory test, valid causal attribution, or calibrated population claim; report what was observed and its provenance, without retrospective significance.
- **Contradicted / null**: preserve the observed result; do not fabricate a repair or claim equivalence merely because a test is nonsignificant.
- **Blocked**: missing run receipt, inconsistent folds/denominators, unverifiable citation passage, untested deployment readout, or another material unresolved conflict; do not promote a stronger statement.

Check the frozen protocol when applicable. Reused calibration/test observations cannot become untouched confirmation just by being rewritten. If a group-constant reward factor appears in a learning claim, trace the actual normalization and gradients before asserting mechanism activation. If a claim depends on other agents, compare appropriate equal-budget and placebo controls when required by that **specific** causal question.

## Lightweight Handoff

The experiment designer owns the estimand and real comparison; the research engineer supplies code and run evidence; the integrity auditor checks claim-support; the paper writer applies allowed wording. The orchestrator coordinates only when an actual multi-stage decision needs it. Retain the conclusion in the manuscript's **existing** results notes or canonical handoff record; avoid a separate process file for each claim.

On a new checked batch, re-evaluate only the affected claims, captions, table cells and Figure Registry entries. The result may justify "narrow", "keep", "retract" or "needs evidence"; none automatically launches training, an independent model, or a remote task.

## Adaptation note

Conceptually informed by [ARIS result-to-claim and research memory](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep), [Claude Scholar research contract](https://github.com/Galaxy-Dawn/claude-scholar), and [Orchestra Research's ARA rigor review](https://github.com/Orchestra-Research/AI-Research-SKILLs). This CCFA gate is independently worded, scoped to existing artifacts, and requires no third-party runtime or stored graph.

## Supplement (Batch-2, 2026-11-03): Source-Type → Claim-Strength Ladder

The promotion record above decides *whether* a result may be promoted. This ladder bounds *how strongly* a source of a given type may be worded, so the check does not depend on reviewer intuition. It governs literature and artifact evidence alike.

**Strength levels** (weakest to strongest): `speculative` → `observed` → `supported` → `strong`. Never promote a claim to a stronger level without naming the evidence that justifies the upgrade; a silent upgrade is a gate failure even when the stronger wording happens to be true.

| Source type | Strongest claim it may support | Conditions |
| --- | --- | --- |
| Abstract-only / webpage placeholder | Discovery and to-read routing only; no manuscript, rebuttal, or durable-conclusion claim | Must be replaced by the full text or a verified artifact before any stronger use |
| Project note / handoff summary | Hypotheses, plans, and motivation wording | Literature-backed claims require a separate evidence locator for the underlying source |
| Full paper / preprint (inspected passage) | `observed` or `supported` | The relevant method, dataset, metric, and limitation are named; identity alone (title/abstract match) supports nothing beyond `observed` |
| Dataset / experiment artifact (own runs) | `observed` to `strong` for project claims | Unit of analysis, metric, provenance, split/seed identity, and analysis limits are recorded |
| Multiple independent anchors, or one anchor plus a checked replication | `strong` | Anchors must be genuinely independent (not the same run re-described) |

**Evidence locator convention.** Where a project already keeps evidence records, identify each with a stable ID of the form `ER-YYYYMMDD-shortslug-NN` and reuse the same ID downstream; create a new ID only for a distinct source, artifact, or analysis result. This is a naming convention for locators inside the existing notes, manifest, or handoff — it does not create a new claim database, consistent with the Lightweight Handoff above.

**Promotion checklist addition.** Before promotion, also confirm: (1) the claim names at least one evidence locator; (2) the source type is strong enough for the intended strength per the ladder; (3) allowed wording and forbidden stronger wording are both recorded; (4) contradictory or missing evidence is preserved, not deleted.

> Provenance: ladder, strength rules, and ID format adapted from Galaxy-Dawn/claude-scholar (MIT License), `skills/research-ideation/references/research-contract.md`, batch-2 integration 2026-11-03. Adapted to this gate's existing-artifacts scope; the upstream Zotero/Obsidian pipeline and its mandatory record files were not imported.
