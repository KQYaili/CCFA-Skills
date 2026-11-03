# Hypothesis Generation: Rivals Before Tests

Use when an observation or preliminary result is being turned into a
research direction — before experiments are designed. The discipline: a
hypothesis is a proposal to be challenged, not a finding. Generate rival
explanations *first*, derive predictions on which the rivals disagree, and
only then choose tests. Skipping the rival step is how a single plausible
story hardens into a project.

## Keep The Objects Distinct

An **observation** (what was measured, with provenance and uncertainty) is
not a **hypothesis** (a candidate explanation); a **prediction** (an
observable implication derived before checking) is not **evidence**;
support for one candidate does not eliminate unconsidered rivals, and
rejecting one null does not prove a mechanism. Novelty is "not located
within the documented search boundary" — never "no prior work exists".

## Step 1 — Freeze The Observation

Write the observation before interpreting it: measurement and source,
system/population, unit of observation and of analysis, uncertainty,
missingness, exclusions, preprocessing — and whether the pattern was
expected, exploratory, or noticed after viewing results. Use "observed" /
"associated", not causal language, unless the design earns it.

## Step 2 — Generate Rivals From Distinct Classes

Produce candidates from genuinely different explanatory classes when
plausible (do not force a fixed count or false symmetry):

1. **Proposed mechanism** — the effect is real and works as theorized.
2. **Measurement or processing artifact** — the pipeline manufactures the
   pattern (export/precision confounds, evaluator drift, normalization
   applied at the wrong stage, leakage in the harness).
3. **Confounding or common cause** — a third variable drives both sides.
4. **Selection or attrition** — the observed subset differs from the target
   population (surviving runs, answered items, non-missing cells).
5. **Collider conditioning** — conditioning on a common effect induces the
   association.
6. **Reverse causation** — the arrow runs the other way.
7. **Temporal / contextual / boundary differences** — the pattern holds
   only in this window, setting, or regime.
8. **Stochastic variation** — noise, multiplicity, or selective reporting
   of looks.
9. **Competing mechanism at another scale** — a different level of the
   system (data, optimizer, interface, population) explains it better.

Keep every candidate labelled `candidate`. Generate an initial set before
any AI-assisted expansion, to reduce anchoring.

## Step 3 — Discriminative Prediction Matrix

For each candidate: the conditions and boundary conditions; the observable
and its measurement; the expected pattern with uncertainty; a result that
would be *incompatible* with the candidate under declared assumptions; and
the contrast against at least one rival. Prefer tests where rivals predict
meaningfully different outcomes; define in advance what an indeterminate
outcome would teach. Keep the matrix as a working table (candidate ×
prediction × discriminating observation).

## Step 4 — Strict Negative Controls

A negative control must be **incapable of operating through the proposed
mechanism while sharing the relevant bias pathways**. An untreated group
that merely omits the intervention is decorative, not a control. A non-null
control result signals an invalid control assumption or a bias pathway —
it does not by itself identify or quantify the bias in the target estimate.
(Placebo arms and isomorphic same-model controls in this repo's experiment
practice are instances of this rule.)

## Step 5 — Preregistration Scaffold

From the surviving candidates, draft the scaffold the experiment designer
will freeze: claim type (descriptive / associational / predictive /
causal / mechanistic); for causal targets, the estimand (population,
intervention and comparator, outcome and horizon, summary measure,
identification assumptions); primary contrast and analysis unit; exclusion
and stopping rules; multiplicity family; what is confirmatory vs
exploratory. The scaffold then follows the
[research-rigor gates](../../ccf-common/references/research-rigor-gates.md):
commit the frozen protocol before the confirmatory batch runs, and power
the primary contrast with
[statistical-power.md](../../ccf-experiment-designer/references/statistical-power.md)
where the design is comparative.

> Provenance: adapted from K-Dense-AI/scientific-agent-skills (MIT License,
> Copyright (c) 2025 K-Dense Inc.), `skills/hypothesis-generation`,
> batch-2 integration 2026-11-03. Rival classes and control discipline are
> upstream's; examples were re-grounded in this repo's ML-experiment
> context. The upstream skill's self-citation clause was **not** imported.
> Its biomedical safety/ethics gating and its script suite were not
> imported; the preregistration scaffold here is a structure, and the
> executable power/design machinery lives with `ccf-experiment-designer`.
