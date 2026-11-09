# Manuscript Quality Audit: 15 Checks + Evidence and Submission Extensions

Use this shared standard for a requested whole-manuscript audit, a substantive argument/evidence alignment review, or final manuscript readiness. For a local prose edit, single figure correction, concept-only review, or an intentionally results-pending draft, check only relevant surfaces. This is **not** a universal CCF-A/CCF-B acceptance rule, an official reviewer form, or permission to rewrite a paper or launch experiments.

## Scope and precedence

1. Apply the exact venue/year/track/stage's **verified current official rules and template** for mandatory formatting, disclosure and submission requirements. Never turn an example from another venue or year into a universal mandate.
2. Treat scientific integrity, accurate evidence and non-fabrication as non-negotiable regardless of venue conventions. Prefer a bounded truthful statement over a sweeping unsupported claim.
3. Follow the author's documented style for matters the venue leaves open, consistently across manuscript, figures, captions and appendices.
4. Use **P0 / P1 / P2 as audit order**, not as the review report's critical/major/minor severity, a score penalty, or a claim of automated completeness. Assign actual severity only after inspecting the consequence. P0: science/argument validity; P1: semantic and visual interpretability; P2: format and editorial consistency.

## The 15 author-supplied audit checks

| ID | Priority | What must be verified |
| --- | --- | --- |
| M01: first-use mathematical notation | P1 | At first meaningful occurrence define variables, indices, subscripts, sets, constants, operators and relevant domains or ranges near the equation. A **where** clause is one clear option, not mandatory after every equation; avoid repeated or conflicting definitions. |
| M02: first-use acronyms | P1 | Expand non-obvious abbreviations at first use, with consistent subsequent spellings. Check whether the abstract and main text each require an independent first expansion under the target convention. |
| M03: authentic application scope | P0 | For application-driven work, identify the real task, actors, context and plausible deployment setting in the abstract; do not manufacture a scenario by stacking conditions that never co-occur. For theory/mechanism work, state the formal setting rather than invent an application. |
| M04: gap and contribution | P0 | State what the closest work already solves, the concrete unresolved gap, why it matters and what this manuscript independently adds. Distinguish a new mechanism, result, problem setting or application from repackaging; neither claim novelty by stitching modules nor dismiss a genuinely new demonstrated combination. |
| M05: experiment-to-claim design | P0 | Every major experiment answers an identified research question or tests a claim. Make the relation between main results, strongest baseline, ablation, mechanism test, robustness check and counterexample explicit (sequential, parallel or discriminating), rather than stacking tables without an argument. |
| M06: interpretation and boundary | P0 | Explain causal alternatives, confounders, failures, practical/statistical meaning and scope; do not paraphrase each row as analysis. Report weak/null/negative outcomes candidly; distinguish confirmed, consistent-with, plausible and speculative explanations. Cautious language cannot replace missing evidence. |
| M07: figure visual grammar | P1 | Across comparable figures, check open/closed spines, grid visibility/weight, fonts, line width, colors, error bars and legend conventions. Use color-vision-deficiency-friendly encodings with shape/line-style redundancy and grayscale legibility; legends must map to methods/conditions without guessing. |
| M08: values and units | P2 | Inspect quantity-unit spacing and SI/venue style (e.g., 10 ms, 32 GB); percent signs, angles, mathematical quantities and venue-specific rules can differ. Do not apply an indiscriminate search-and-replace. |
| M09: multi-line equation grouping | P2 | Check numbering, mathematical relationships and alignment. Use cases or a left brace only when the equations form a piecewise definition/system or meaningful brace group; use aligned/gathered for derivations or lines that share a number without that semantics. |
| M10: cross-modal symbols | P1 | Match variables, capitalization, subscripts, units, dataset/model names and metric direction among prose, equations, pseudocode, tables, plot labels, legends and appendices. |
| M11: bibliography correctness | P2 | Verify citation keys, metadata, author/year/venue/DOI/version and bibliography style against the chosen template; check unresolved or orphan references and inconsistent published/preprint versions. |
| M12: citation support for the gap | P0 | For closest prior work, novelty, first/only/SOTA and gap statements, inspect actual directly relevant sources rather than citation counts, broad surveys or venue prestige alone. Label unsupported or unchecked positioning, and do not infer low scientific quality solely from a journal tier. |
| M13: headings and subfigure captions | P2 | Apply venue-defined Title Case or sentence case consistently. If the caption refers to panels (a), (b), (c), etc., verify the letters exist and match their order on the actual figure; keep caption punctuation conventions consistent where semantically appropriate. |
| M14: hyphens and dashes | P2 | Inspect spurious hyphens, line-break artifacts and inconsistent compounds; distinguish hyphen, en dash, em dash and mathematical minus according to meaning and target house style. |
| M15: semantic tense consistency | P1 | Avoid accidental tense/voice shifts in a passage; permit present tense for general truths/current figures and past tense for completed experiments or prior work where the meaning warrants it. Do not impose one tense on every sentence. |

## Four additional evidence checks

- **E01 — Claim/evidence alignment (P0):** Trace every abstract/introduction/conclusion contribution to a proof, protocol, results table or inspected evidence; separate **measured performance**, **validated mechanism**, and **demonstrated transfer scope**. Observation is not causation; non-significance is not proof of equivalence. Use the existing [claim-promotion gate](claim-promotion-gate.md) for consequential promotions.
- **E02 — Fair comparisons (P0):** Inspect baseline strength, model ability, task/seed pairing, tuning budgets, training and inference calls/tokens, hardware, selection rules, leakage and denominators. Disclose or limit conclusions where conditions are not comparable.
- **E03 — Uncertainty and inference (P0):** Where the study calls for it, distinguish exploratory and confirmatory outcomes, effect size, interval/variance, paired unit, multiple testing, and statistical from practical importance. Do not require a specific p-value, seed count or interval for every contribution type. Use [research-rigor-gates.md](research-rigor-gates.md).
- **E04 — Reproducibility and falsifiability (P0):** Locate source/protocol version, evaluation unit, data and code dependencies, exact implementation, randomness, analysis logic and decisive controls or counterexamples. A missing item is not automatically an instruction to start a new run.

## Six further safeguards from the consolidated review notes

- **X01 — Number provenance (P1, P0 if decision-changing):** Each important numerical statement in abstract, introduction and conclusion should point to the underlying table/figure/result record. Check rounding, numerator and denominator, slope/axis units, **percentage vs percentage points**, and consistency across all occurrences. A source-less number is not rescued by fluent wording.
- **X02 — Self-contained captions (P1):** On the rendered figure, identify every panel and explain error bars/shading, sample size or unit of analysis, significance markers, and bold/highlight semantics when used. Readers should not have to guess these encodings from unrelated text.
- **X03 — Closest-work freshness (P0):** For a submission-ready novelty or gap claim, refresh the nearest-neighbor literature check when browsing is authorized and it is materially stale; verify relevant new publications and versions and distinguish a found predecessor from a speculative collision. Without access, mark the freshness check unverified, not passed.
- **X04 — Sibling-manuscript overlap (P0):** For related papers, map reused experiments, datasets, text and figures to each manuscript's independently defensible contribution. Disclose/cite shared provenance as required; check overlapping-submission and duplicate-publication rules for the actual venues. Shared evidence does not itself prove unethical duplication, but cannot be repackaged as independent confirmation.
- **X05 — Anonymity, release claims and declarations (P1 / venue-specific):** Verify the current submission stage and mandated anonymity, conflicts, author-contribution, and acknowledgment requirements. Reconcile statements such as “code available,” “will release,” and “DOI” with actual authorization and artifacts. Never reveal private repository identities or promise a public release without approval.
- **X06 — Versioned review receipt (process):** Tie material findings to the exact manuscript version/commit and inspected sections; carry stable finding IDs and state **not checked** explicitly. A former-version audit is not a pass for a new revision, and a parser/regex candidate is not an observed defect until counterchecked.

## Execution and output

1. Reconstruct the paper's claim chain from abstract → introduction → closest work → method → experiments/proofs → conclusions/limitations. Apply **P0 first**, narrowing unsupported claims before copyediting. For a writing-only scope, report scientific questions as unverified dependencies rather than inventing a full scientific verdict.
2. Check P1 at the actual source **and rendered final size** where available: symbol and acronym first use; figure legend/panel/caption correspondence; number, unit and semantics across text/plots. For iterative projects preserve stable figure labels, evidence-backed incremental performance figures and the [method-freeze figure gate](research-figure-lifecycle.md).
3. Check P2 against the **verified venue template**, using a real LaTeX build/PDF when possible. Unavailable source/build is **not checked**, not “passed”. Do not mistake cosmetic consistency for scientific validation.
4. Return a located finding, not a vague “improve clarity” instruction:

| Field | Required meaning |
| --- | --- |
| Finding ID and rule | Stable ID, M01–M15 / E01–E04 / X01–X06, audit priority and separately justified review severity |
| Location and version | Exact paper/section/line or equation/figure/table + manuscript version |
| Observed basis | Inspected wording, source, number, rendered artifact or verified venue rule; note coverage limits |
| Why it matters | Concrete scientific, interpretive or compliance risk and strongest countercheck performed |
| Minimum repair | Specific correction or narrower claim; no new data/author decisions invented |
| Next verification | Text only / source or CPU recheck / additional scientific evidence requiring authorization / not checked |
| Status | Open / resolved and rechecked / awaiting evidence / not checked |

Keep the existing reviewer report template and scorecard; this table describes the **substance of findings**, not a replacement report. Apply only the checks matching the user-requested mode. A checklist cannot certify acceptance, venue compliance, scientific validity, independent review, or permission to publish.
