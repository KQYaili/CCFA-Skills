# Reverse Outline and Scientific Claim Chain

Use for a substantial manuscript **writing/full review** when the scientific storyline is fragmented, overly implementation-led, or when the user requests a claim-to-experiment audit. This is an optional diagnostic, **not** a new review report, a score rubric, or a requirement to run experiments. The owner is `ccf-paper-reviewer`; integrate findings into its normal report. A writer may use the located structural problems to make separately authorized edits.

## 1. Reconstruct the argument before judging style

Read the supplied manuscript at the requested coverage, including abstract, introduction, contribution statements, section headings, result paragraphs, figures and captions, and conclusion. Inspect supporting results or references when available. State explicitly when a section, appendix, source, or experiment was **not inspected**. Distinguish a documented claim from an inferred rationale.

In one sentence each, record the paper's **scientific question**, **contribution type** (method, empirical mechanism, theory, dataset, systems result, etc.), **main counterfactual or baseline**, and **scope**. Do not presume that every contribution must beat every baseline; an informative negative result or boundary characterization can be central.

## 2. Reverse-outline the actual paragraphs

For each paragraph in the inspected sections, privately record:

| Location | Opening claim / paragraph job | Needed evidence or prior premise | Connection to preceding paragraph |
| --- | --- | --- | --- |
| Section + paragraph index | Problem, prior work, hypothesis, mechanism, protocol, finding, alternative, boundary, or implication | Exact result, proof, source, or missing basis | Continues / redirects / jumps / repeats |

Read the sequence of paragraph openings **without their body text**. Ask whether a reader could recover the scientific problem, why the prior account is insufficient, the proposed explanation or intervention, what evidence distinguishes it, and what remains unproven.

Flag only consequential structural defects: a missing causal bridge, an observation promoted to a mechanism, a new contribution introduced after results, redundant setup, or a conclusion that never answers the stated question. A paragraph may correctly start with an equation, definition, or transition rather than a literal topic sentence. Do **not** automatically rewrite every paragraph or enforce one rhetorical template.

## 3. Map prominent claims to evidence and competing accounts

Audit important claims in the abstract, introduction, figure captions, and conclusion against the actual paper; reuse the shared [manuscript audit](../../ccf-common/references/manuscript-audit-standard.md) and [claim-promotion gate](../../ccf-common/references/claim-promotion-gate.md).

| Claim and location | Evidence location + design status | Rival explanation or limitation | Finding |
| --- | --- | --- | --- |
| Concrete, bounded claim | Figure/table/proof/record; preregistered, exploratory, or uninspected | What the same observation cannot rule out | Supported / qualified / needs evidence / contradicted / not inspected |

Do not treat an exact algebraic decomposition as an identified causal mechanism. A statistical association is not a prospective prediction. A null interval is not proof of equivalence. Attribute inference strength to the experimental design, not the elegance of the wording.

For a paper organized around research questions, check: **phenomenon (what?) → explanatory distinction (why?) → limits (when?)**. These are optional layers, not three obligatory contributions or experiments. If the evidence cannot separate rival explanations, recommend a narrower claim or name one decision-changing prospective test; do not create a generic ablation shopping list.

## 4. Check five lenses without replacing the venue rubric

1. **Contribution-to-question fit:** Does each claimed contribution answer the declared question?
2. **Story clarity:** Do paragraph functions and transitions build one defensible argument?
3. **Evidence-to-RQ fit:** Do measurements, proof obligations, or case studies resolve the question actually asked?
4. **Evaluation validity:** Are strong comparators, data units, costs, uncertainty, and leakage boundaries handled at the level the claim needs?
5. **Method and mechanism rationale:** Are design choices motivated and can their asserted necessity be checked or bounded?

These are **inspection lenses**, not a new scorecard. Keep the venue-specific rubric, review severity, and standard output format. Inspect a plausible counterargument in the source before raising a major claim. Do not judge a mechanism-oriented or negative-result paper solely by whether it wins every benchmark.

## 5. Report only decisions that change the paper

Return a short sequence of located, evidence-bound findings, each with **problem → why it matters → smallest honest repair** (restructure, relocate, qualify, cite, or request a discriminator). Preserve the existing concern IDs and review scope. A writing-only pass may report argument structure but must not certify empirical validity.

### Provenance

Workflow inspiration: [ResearchPilot-Skills](https://github.com/LMDHQ-0420/ResearchPilot-Skills), stage `research[G.7]-review` (MIT-licensed). This is a CCFA-specific, independently rewritten adaptation; it does not import ResearchPilot's mandatory phase gates, scoring template, or universal “beat all baselines” criterion.
