# Benchmark Paper: Genre Template

Use when the manuscript's main contribution is an evaluation dimension, a
dataset/benchmark, or a measurement framework — not a new algorithm. A
benchmark paper wins by defining what will be measured and shipping a
construction pipeline that makes the measurement high-quality, scalable,
and reproducible. Structure the draft around five pillars; a missing pillar
is the first thing reviewers find.

## The Five Pillars

1. **Research gap.** The evaluation dimension existing work misses, grounded
   in a concrete failure case. Name at most three prior benchmarks and the
   specific blind spot of each; vague "is limited" phrasing does not count.
2. **Construction pipeline.** How the data is built: source selection,
   generation, annotation, quality control, split strategy, statistical
   profile.
3. **Evaluation framework.** Fine-grained by design (below), not one overall
   score.
4. **Empirical findings.** Multi-angle comparisons (human vs model,
   architecture families, error distributions) condensed into bolded
   *Finding X:* statements that read like lemmas and are actionable for
   future work.
5. **Companion method (optional, strongly recommended).** A model or method
   trained/tuned on the benchmark's unique signal, showing the community
   can act on the findings.

## Design Goals (state all four explicitly)

| Goal | Content | Typical strategy |
| --- | --- | --- |
| G1 Coverage | The benchmark spans the breadth of the target capability | Systematic taxonomy, diverse sources, stratified sampling |
| G2 Fine-grained diagnostics | It pinpoints *where* models fail, not only *whether* | Multi-dimensional taxonomy with sub-categories and difficulty levels |
| G3 Scalability | Construction is reproducible and extensible at low cost | Automated/semi-automated pipeline, minimal manual annotation |
| G4 Quality | Annotations are accurate and evaluation is reliable | Multi-stage QC, inter-annotator agreement, expert validation |

## Task Scope

State both sides of the boundary, in the paper: what is evaluated, and what
is explicitly **not** evaluated with the reason (different research
question; already covered; out of the construct's definition). This
pre-empts the reviewer's "why didn't you include X?".

## Taxonomy And Construction

Pick one taxonomy pattern and say why it fits: **capability × difficulty**
matrix; **phenomenon type × severity** spectrum; or **multi-dimensional
quality framework** (top dimensions decomposed into measurable
sub-dimensions). Count the resulting evaluation cells; the taxonomy is the
backbone of the diagnostics claim (G2).

Construction follows one of three paradigms — name it and justify it:
**reverse synthesis** (seed knowledge, then instantiate items);
**controlled injection** (seed items, then inject targeted ambiguity,
noise, or error); **adaptive generation with expert validation** (model
generation filtered and corrected by experts).

The evaluation framework table lists, per sub-dimension: metric, scoring
method, range, automation level. Decide explicitly: automatic vs
LLM-as-Judge vs human scoring (an LLM judge **must** be validated against
human judgments); single vs multiple valid answers; scoring granularity.

## Two First-Class Design Elements

Treat these as design sections, not limitations-section afterthoughts:

- **Contamination mitigation.** Address each applicable type: training
  contamination (benchmark items inside model training sets — mitigate by
  time-gated construction, synthetic generation, novel sources); prompt
  contamination (evaluation prompts leaking — unique templates, private
  evaluation scripts); contamination laundering (synthetic data generated
  *by* contaminated models — verify provenance, cross-check against
  non-LLM sources); saturation over time (versioning and extensibility
  plan).
- **Difficulty calibration.** State the expected top-model score at launch
  and a difficulty sanity check: a commonly cited heuristic is that the
  strongest models should reach only roughly 0.1–9% on the hardest subset
  at launch; if top models already exceed ~50% overall, the benchmark may
  be born saturated. Include difficulty headroom for future models.

## Paper Structure

Introduction as a six-part chain: background + running example (Figure 1) →
existing-benchmark limitations (≤3) → research questions (2–3) → design
considerations → proposal → contributions (typically four: benchmark,
pipeline innovation, systematic evaluation, findings or companion method).
Then: §2 task + design goals; §3 construction pipeline (Figure 2);
§4 companion method (optional); §5 experiments organized by research
question, with the overall-performance table (usually the largest in the
paper), fine-grained analysis, a human baseline when available, and the
bolded findings; §6 discussion and research opportunities; §7 related work
with a benchmark comparison table (essential — often Table 1).

Before drafting, the [contribution contract](contribution-contract.md)
applies as usual: for this genre the core statement names the evaluation
dimension and the diagnostic claim, not a method's accuracy.

> Provenance: independently worded adaptation of the benchmark-paper
> framework in HKUSTDial/Supervisor-Skills, `skills/benchmark-paper-template`
> (skill declares CC BY 4.0; mixed licensing across the source repo —
> principles and structure only, no prose, tables, or checklist text
> copied), batch-2 integration 2026-11-03.
