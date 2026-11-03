# Result-to-Claim Gate

> Provenance: adapted from wanshuiyin/Auto-claude-code-research-in-sleep
> (ARIS), `skills/result-to-claim/SKILL.md` and
> `skills/shared-references/evidence-precheck.md` (MIT License, Copyright
> (c) 2026 wanshuiyin). All vendor backend names were replaced with the
> generic role "independent cross-model reviewer"; ARIS-specific routing,
> wiki, and scheduling machinery was dropped. The two-stage design follows
> the reconcile pattern: a model's self-report is cross-checked against
> mechanical ground truth before any judgment call is spent on it.

Experiments produce numbers; this gate decides what those numbers are
allowed to *mean* before drafting turns them into claims. It runs after a
set of experiments completes and before the results are written into a
manuscript, a review response, or a project decision. It is a gate, not a
review: `ccf-paper-reviewer` still owns full scientific judgment of a
draft, and this gate's verdicts are recorded inputs to that review, not
substitutes for it.

## Relation to the claim promotion gate

`ccf-common/references/claim-promotion-gate.md` owns the promotion
decision: whether a material result may enter a manuscript, abstract,
caption, or rebuttal, and at what bounded wording and status. This
auditor-side protocol is that gate's mechanical front-end for empirical
results: Stage 1 verifies that cited evidence actually exists, Stage 2
routes each intended claim as `yes` / `partial` / `no`, and the routing
record feeds the promotion record the common gate requires. Where the
two appear to conflict, the common gate's decisions govern wording and
status; this protocol governs evidence existence and support routing
only.

## Verdict vocabulary

Each intended claim leaves the gate with exactly one routing verdict:

- `yes` — the results support the claim as stated.
- `partial` — the results support a narrower or weaker claim; the gate
  records the supported revision.
- `no` — the results do not support the claim. **`no` is a first-class
  outcome**, recorded with the same care as a confirmation: what was
  tested, what failed, the leading hypotheses for why, and the constraints
  this places on future attempts. A `no` is never rounded up, softened, or
  retried by re-asking until it changes.

## Stage 1 — Deterministic evidence pre-check (no model call)

For every claim that cites a specific value and a source file:

1. Build the claims list as JSON: `[{"id", "value", "source"}, ...]`,
   where `source` is the result file or glob relative to the project root
   and `value` is the cited number or string.
2. Run `scripts/evidence_check.py <project-root> --batch <claims.json>`.
   Statuses per claim: `verified` (the cited value appears in the cited
   file), `path_missing`, `value_not_found`, `unparseable` (no usable
   value/source pair).
3. Act on the statuses before any judgment is spent:
   - `path_missing` / `value_not_found` = hallucinated evidence. The claim
     is marked **unsupported — evidence not found** and routed `no`
     immediately. Do not spend a reviewer call defending a number that is
     not in the data; a deterministic rejection needs no reviewer.
   - `verified` means **only that the cited evidence exists** — never that
     the claim holds. Existence is execution-completeness; support is a
     quality verdict reserved for Stage 2.
   - `unparseable` claims proceed to Stage 2 normally.
4. Carry the per-claim pre-check status into Stage 2, so the reviewer sees
   which claims have real evidence to read. If the pre-check could not run
   (helper unavailable), say so explicitly in the gate record instead of
   omitting the stage.

The matcher is deliberately conservative (exact decimal equality on
safely-bounded numeric tokens; fail-closed on compound constructs such as
dates, versions, and locale groupings): a false negative costs one reviewer
read, a false `verified` is the failure this stage exists to prevent.

## Stage 2 — Independent cross-model support judgment

The support judgment must be made by an **independent cross-model
reviewer**: a reviewer from a different model family than the one that
produced the claims, in a fresh context, reading the artifacts itself (the
pre-check flags what to read; it never pre-digests the verdict). This is a
Type-B value gate under [loop-governance.md](../../ccf-common/references/loop-governance.md):
the executing agent may DRIVE the gate but may not ACQUIT its own claims.

Give the reviewer, for each intended claim: the claim text; the experiments
run (method, dataset, configuration); the key results with baseline
comparisons and deltas; the Stage-1 status table; the baselines' provenance
(reproduced vs. reported); and the known caveats and confounds. Ask for:

```text
claim_supported: yes | partial | no
what_results_support: what the data actually shows
what_results_dont_support: where the data falls short of the claim
missing_evidence: specific evidence gaps
suggested_claim_revision: strengthened / weakened / reframed wording, if any
next_experiments_needed: specific experiments that would fill the gaps
confidence: high | medium | low
```

Rules for the judgment:

- Do not inflate claims beyond what the data supports; if the reviewer
  says `partial`, do not round up to `yes`.
- A single positive result on one dataset does not support a general claim;
  scope is part of the verdict.
- If confidence is `low`, treat the judgment as inconclusive: add evidence
  rather than committing to the claim.
- If an experiment-integrity audit exists for these results (see
  `ccf-experiment-designer/references/experiment-audit.md`), attach its
  status: `fail` appends an integrity concern to the verdict and caps
  confidence at `low`; `warn` is flagged; no audit run labels the verdict
  "provisional — no integrity audit run" without blocking the gate.
- **Fail closed if the reviewer is unavailable.** If no independent
  cross-model reviewer can be reached, the gate outputs
  `verdict: REVIEW_UNAVAILABLE` and stops: the executing agent never
  substitutes its own claim judgment, and no downstream step (drafting,
  ablation planning, claim records) may consume a run that lacks a verdict.
  The only exception is Stage 1's deterministic rejection of hallucinated
  evidence, which stands on its own.

## Stage 3 — Routing

- `no`: record the postmortem with the evidence (tested, failed, why,
  constraints for future attempts). The claim does not enter any draft.
  Decide explicitly whether the line is closed or an alternative approach
  is authorized as a new test with its own evidence.
- `partial`: adopt the supported revision as the working claim, record the
  gap, and design supplementary experiments against the named missing
  evidence. Re-run this gate after they complete. Repeated `partial`
  verdicts on the same claim trigger an explicit scope decision: narrow
  the claim or close the line.
- `yes`: the claim may proceed to drafting. Record the verdict, the
  evidence anchors, and the confidence with the results so the drafting
  owner and later audits inherit them.

Record every verdict and its reasoning with the experiment record,
regardless of outcome. The gate is run once per result set; re-running it
on a timer adds no signal — the verdict changes only when the results do.
