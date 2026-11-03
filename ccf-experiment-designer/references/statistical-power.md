# Statistical Power Discipline (Design-Time)

> Provenance: discipline adapted from K-Dense-AI/scientific-agent-skills,
> `skills/statistical-power/SKILL.md` (MIT License, Copyright (c) 2025
> K-Dense Inc.); scripts `power.py` / `simulate_power.py` in `../scripts/`
> are copied from the same skill. The source skill's self-citation
> requirement is not carried over. Effect-size conversion tables and
> per-test argument recipes from the source references were not imported;
> the scripts' docstrings document their own interfaces.

Use this in the preregistration / design step of `ccf-experiment-designer`,
especially when a confirmatory run is expensive (paid compute, limited
seeds, human subjects) and a contrast must be powered *as its own primary
question*: a contrast that is only powered as a by-product of a larger
design is exploratory, and the preregistration must say so.

Four quantities are locked together for any test — sample size `n`, effect
size, significance level `α`, and power `1 − β`. Fixing three solves for
the fourth. Every use of the scripts is a rearrangement of that identity.

## Dependencies

- `scripts/power.py`: Python ≥ 3.12, `statsmodels`, `scipy`, `numpy`
  (source tested with statsmodels 0.15.0 / scipy 1.18.1). Closed-form
  solvers for `t_ind`, `t_paired`/`t_one`, `anova`, `two_proportions`,
  `one_proportion`, `correlation`, `chi2`, `linear_regression`, exposing
  `sample_size(...)`, `power(...)`, `mde(...)`, `power_curve(...)`.
- `scripts/simulate_power.py`: `numpy` (plus whatever the caller's
  generate-and-test callback needs). Monte Carlo harness with
  `simulate_power()` and worked examples for designs closed forms do not
  fit (GLMs, mixed models, clustering, interactions).

If the dependencies are unavailable in the working environment, say so and
plan qualitatively — do not hand-compute a substitute and present it as a
power analysis.

## The discipline

1. **SESOI first.** The effect size is chosen before any calculation, in
   this order of preference:
   - the smallest effect size of interest (SESOI) — the smallest effect
     that would change the decision the experiment feeds;
   - a pilot or prior-study estimate, treated as uncertain (see 4);
   - a convention (Cohen's small/medium/large) only as a last resort, and
     labelled as such.
   Never invent an effect size to make the arithmetic come out affordable.
2. **Sensitivity analysis is mandatory.** Report required `n` (or achieved
   power / MDE) across a plausible *range* of effect sizes — a power
   curve, not a single number. A power analysis presented as one number
   hides its largest source of uncertainty.
3. **Post-hoc ("observed") power is refused.** Computing power from the
   effect size just observed is circular — it largely restates the
   p-value and adds no evidence about adequacy. If a run is finished and
   the question is what it could have detected, report the MDE at the
   achieved `n` (a sensitivity statement) or the confidence interval
   around the observed effect instead. If asked for observed power,
   flag this and offer the MDE/CI form.
4. **Pilot estimates are inflated.** Small pilots are imprecise, and
   significance- or publication-based selection biases pilot effects
   upward. Powering a confirmatory run on a raw pilot point estimate
   systematically underpowers it; use a shrunken value or a sensitivity
   range whose low end reflects the pilot's uncertainty.
5. **Adjustments are explicit.** State how the calculation handled:
   multiplicity (power primary contrasts at the corrected α when a
   correction is planned), attrition/unusable runs (inflate the *planned*
   n, since power governs the *analyzed* n), clustering / non-independent
   units (treating correlated measurements as independent is
   pseudoreplication and badly overstates power — simulate instead), and
   one- vs two-sided tests (two-sided is the default; justify any
   one-sided choice).
6. **Match the method to the planned analysis.** A t-test formula does
   not power a logistic regression or a mixed model. When closed-form
   assumptions do not fit the planned analysis, use
   `scripts/simulate_power.py`: simulate from the assumed truth, analyze
   with the *exact* planned test, repeat ≥ 1,000 times (5,000–10,000 near
   80% power), and report the Monte Carlo confidence interval the harness
   returns. First check Type I error under the null.

## Reporting

A defensible power statement names every input so a reader can reproduce
it: the test and its exact planned form, the effect size and its basis
(SESOI / pilot / convention), α and sidedness, target power, the resulting
n (analyzed and planned, after adjustments), the sensitivity range, and
the tool versions. Record it in the preregistration or design document —
not as a post-hoc paragraph written after the results are known.
