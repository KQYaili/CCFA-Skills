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
