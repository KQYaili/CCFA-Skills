# Exploration Integrity And Scope Calibration Audit

Use when auditing a completed or nearly completed study whose claims rest on
a documented exploration history — preregistrations, run logs, closure
（封井） records, and decision notes. Two dimensions, adapted from
exploration-tree review to CCFA's records: **exploration completeness**
(was the search process honest and complete?) and **scope calibration**
(do the claims assert exactly what the evidence supports?).

## Inputs

- The preregistration or protocol record, including any amendments.
- The run/experiment log: every attempted route, including stopped and
  failed ones, with the recorded reason for stopping.
- Closure records: routes formally closed, with the closing evidence.
- The claim list under audit (manuscript claims, abstract, captions).

If no exploration record exists, report that as the finding — this audit
cannot be run from the manuscript alone, and its absence is itself an
exploration-integrity gap for any confirmatory claim.

## D5 — Exploration Completeness

Check, in order:

1. **Dead-end quality.** Each abandoned route records a specific failure
   mode and a transferable lesson. "Didn't work" is not a failure mode;
   "diverged after the teammate-miss term entered the advantage, gradient
   norm ×40" is.
2. **Decision rationale.** At each recorded decision, the chosen path is
   justified against real alternatives that were actually considered, not
   strawmen reconstructed afterwards.
3. **Rebutted-branch consistency (hard contradiction).** No claim advocates
   a route, configuration, or interpretation that the record marks as a
   dead end or closed. A claim praising a closed route is a logical
   contradiction between the record and the manuscript — flag it at the
   highest severity this audit issues.
4. **Exploration breadth.** For each headline design choice, at least two
   alternatives were considered and documented, or the record states why
   the choice was forced.
5. **Honesty signal.** A record with **zero dead ends**, or only trivial
   failures, is suspicious: real exploration of a non-trivial question
   produces substantive failures. Treat a spotless record as a prompt to
   ask what was omitted, not as evidence of a clean run.

## D3 — Scope Calibration

1. **Over-claiming.** Universal scope markers ("all models", "any dataset",
   "in general") over evidence gathered under specific, narrow conditions.
   The gap must be substantial to flag; ordinary summary compression is not
   over-claiming.
2. **Under-claiming.** Material results present in the record that no claim
   captures — evidence without a corresponding claim is a reporting gap in
   the other direction.
3. **Assumption explicitness.** Assumptions the design silently relies on
   (data distribution, evaluator behaviour, budget parity) are stated, or
   flagged as unstated.
4. **Generalization boundaries.** The claims or limitations state what the
   results do **not** apply to.
5. **Qualifier consistency.** Hedging in the claims ("tends to", "in most
   cases") matches the actual evidence strength — neither stronger nor
   weaker than the record supports.

## Output

Per dimension: the checks that ran, each finding with its record location
(file and entry) and the claim it touches, and a severity. This audit feeds
the [claim-promotion gate](../../ccf-common/references/claim-promotion-gate.md):
a rebutted-branch contradiction or a substantial scope gap blocks promotion
until the wording or the record is reconciled. It does not assign accept /
reject recommendations and does not replace the result-to-claim gate, which
judges individual result→claim support.

> Provenance: adapted from Orchestra-Research/AI-Research-SKILLs (MIT
> License), `22-agent-native-research-artifact/rigor-reviewer` dimensions
> D5 (Exploration Integrity) and D3 (Scope Calibration), batch-2 integration
> 2026-11-03. The input substrate was changed from ARA exploration trees to
> CCFA preregistration / run-log / closure records; the ARA artifact format,
> its scoring anchors, and the other four dimensions were not imported.
