# Novelty Collision Audit (Concept-Only)

Use when the decision depends on **one particular novelty claim** colliding with prior work. Owner: \`ccf-idea-reviewer\`; \`ccf-literature-searcher\` retrieves and anchors the closest original sources. This is a focused extension of [strict-idea-review.md](strict-idea-review.md), not a new report, numeric score or required stage for every idea. Do not request experiment results merely to assess a concept.

## Frame the actual claim

Write separately, using the user's terminology:

- **Problem:** the phenomenon, question or missing capability.
- **Mechanism:** the operation or explanatory principle actually proposed.
- **Claimed delta:** which assumption, operation, inference or boundary is claimed to be new.
- **Consequences and boundary:** what would follow *if* the claim holds, and where it may not hold.

Distinguish a novel scientific inference from a routine implementation combination, new setting, changed hyperparameter or convenient rephrasing. Keep an explicit "not enough to judge yet" outcome if the proposed mechanism itself is unspecified.

## Search by three different failure modes

For a substantial novelty check, build public-safe searches covering:

1. **Same problem:** established treatments of the identical bottleneck, even with different terminology.
2. **Same mechanism:** identical or analogous mathematical operation / counterfactual / assumption, including older and neighboring-field work.
3. **Same purported contribution:** alternative keywords for the paper's strongest distinctive claim; include relevant recent close work.

Use the user's scope, known sources and cost constraints. These are query *roles*, not mandatory query counts or a fixed paper quota. Reuse prior grounded searches; protect private source phrasing per Common's privacy policy. If browsing is disallowed, only use supplied papers and explicitly label the coverage \`supplied-only\`.

Screen using titles/abstracts, but prioritize papers with mechanism overlap, ambiguous assumptions or close novelty claims for relevant **full-method reading**. A title/abstract match is a lead, not a collision verdict. Model recall only supplies search leads; resolve each lead against a real source before it supports a finding.

## Four-axis collision matrix

For each decisive candidate, retain the source URL/version and *what was read*:

| Axis | Question |
| --- | --- |
| Problem | Is the motivating problem or experimental target effectively the same? |
| Mechanism | Does the work already implement or prove the key operation/derivation? |
| Claim | Does it already make the purported scientific inference or intended improvement claim? |
| Boundary / setting | Are assumptions, inputs, evaluation target, costs and valid domains materially equivalent? |

Record overlap as \`same\`, \`partial\`, \`different\` or \`not assessed\` **per axis**, with a page/section/equation anchor where available. Do not sum these labels into a fake quantitative novelty score. Mechanism and claim collisions may be decisive even when domain differs. Conversely, identical wording in introductions does not establish identical mechanisms.

For candidates inspected only by abstract, record \`abstract-only\` beside the evidence and make the collision result **provisional**. Do not silently infer uninspected formulae. Distinguish:

- **Demonstrated collision:** inspected source contains the same central claim under materially equivalent assumptions.
- **Partial overlap / narrower delta:** some components are old; a concrete difference remains to be evaluated.
- **No collision found in inspected scope:** *not* a global claim that the idea is unprecedented.
- **Unresolved:** necessary source or mechanism text was unavailable or contradictory.

## Decision-ready handoff

Return to the integrating reviewer a small table: closest source, inspected location, four-axis overlap, the **surviving one-sentence delta**, coverage, and the *single most informative next reading or conceptual counterexample* when unresolved.

A delta must be phrased falsifiably: "Unlike X, we hold [quantity] fixed while [operation] changes, predicting [consequence] under [assumptions]." This is a **hypothesis** until appropriate evidence exists. If the novelty collapses, say so and propose a narrower honest contribution; do not manufacture significance or make stronger baselines compulsory for a concept-only review.

## Source and licensing note

Original CCFA procedure inspired by the problem/mechanism/claim comparison in [ResearchStudio-Web](https://github.com/CrepuscularIRIS/ResearchStudio-Web) (MIT); the four-axis boundary and reporting contract here are independently authored. Do not copy upstream vendored system prompts or add prompt-parity/content-hash machinery.
