# Experiment Audit (Post-Run Integrity Acceptance)

> Provenance: adapted from wanshuiyin/Auto-claude-code-research-in-sleep
> (ARIS), `skills/experiment-audit/SKILL.md` (MIT License, Copyright
> (c) 2026 wanshuiyin). Vendor backend names, reviewer-routing machinery,
> and ARIS pipeline hooks were replaced with CCFA roles; the six checks and
> their fail conditions are carried over.

Run this audit after a set of experiments completes and before its results
are routed to claims (see the result-to-claim gate in
`ccf-integrity-auditor/references/result-to-claim-gate.md`). It audits the
experiment *artifacts* — evaluation code, result files, ground-truth
provenance — not the manuscript text. `ccf-experiment-designer` owns the
design; this is the downstream acceptance step for what was actually run.

## Independence rule

The agent that ran the experiments collects artifact paths only; it does
not summarize, interpret, or judge them. The audit judgment is made by an
**independent cross-model reviewer** (a different model family, fresh
context) that reads the files directly. This is a Type-B value gate under
`ccf-common/references/loop-governance.md`: the executor may DRIVE the
audit, never ACQUIT its own experiments. If no independent reviewer is
available, the audit reports `REVIEW_UNAVAILABLE` and the results stay
labelled unaudited — the executor never substitutes its own verdict.

Start from the assumption that the evaluation is compromised somewhere;
the audit's job is to find where. The failure modes it targets are usually
not deliberate deception but optimizing-agent failure modes: synthetic
"ground truth" derived from model outputs, metrics normalized by the
model's own statistics, numbers claimed from files that do not exist, and
pilot-scale scope described as comprehensive.

## Artifact collection (executor)

List, without reading or summarizing content:

1. Evaluation scripts (`*eval*.py`, `*metric*.py`, `*benchmark*.py`, test
   harnesses).
2. Result files (`*.json`, `*.csv` under results/outputs/logs) and run
   records or receipts.
3. Ground-truth references inside the evaluation scripts (dataset paths,
   GT loaders).
4. Experiment tracker / log, if any.
5. The claims the results are meant to support (draft sections, narrative
   report, or the gate's claims list).
6. Config files carrying metric definitions.

## The six checks

For each check the reviewer reports `PASS | WARN | FAIL` with exact
file:line evidence.

### A. Ground-truth provenance

Where does "ground truth" / "reference" / "target" come from in each
evaluation script — loaded from the dataset, or generated/derived from
model outputs? If derived, is it explicitly labelled as proxy evaluation?
Are official evaluation scripts used when the benchmark provides them?
**FAIL** if ground truth is derived from model outputs without explicit
proxy labelling.

### B. Post-hoc normalization

Is any metric divided by the max/min/mean of the model's *own* output, or
otherwise rescaled after the fact in a way that inflates it? Are raw scores
reported alongside any normalized scores? Are any scores suspiciously
close to 1.0 / 100%? **FAIL** if a normalization denominator comes from
prediction statistics. (Preregistered, design-time normalization declared
in the protocol is not post-hoc; the check targets undisclosed or
result-dependent rescaling.)

### C. Result-file existence

For each claimed result: does the referenced result file exist, does the
claimed metric key exist in it, does the claimed number match the file,
and is the run's status actually complete (not planned/running)?
**FAIL** if claimed results reference nonexistent files or mismatched
numbers. The deterministic half of this check is mechanized by
`ccf-integrity-auditor/scripts/evidence_check.py`.

### D. Dead code in evaluation

For each metric function defined in the evaluation scripts: is it actually
called by an evaluation pipeline, and does its output appear in a result
file? **WARN** if metric functions exist but are never called — defined is
not the same as run.

### E. Scope of conclusions

How many datasets/scenes/configurations were actually tested, and how
many seeds/runs per configuration? Does the claim language ("comprehensive",
"extensive", "robust", "in general") exceed that scope? **WARN** if the
scope language exceeds the evidence; the fix is narrowing the claim, not
inflating the audit.

### F. Evaluation type labelling

Classify each evaluation and record the label with the results:

- `real_gt` — dataset-provided ground truth;
- `synthetic_proxy` — model-generated reference;
- `self_supervised_proxy` — no ground truth by design;
- `simulation_only` — simulated environment;
- `human_eval` — human judges.

A `synthetic_proxy` (or any non-`real_gt`) result must keep its label
through every downstream claim, table, and abstract sentence; presenting a
proxy evaluation as if it were `real_gt` is a **FAIL** under check A/F.

## Output

Write the audit beside the experiment record (project workfiles, not the
skill directory):

```text
Overall verdict: PASS | WARN | FAIL
Integrity status: pass | warn | fail
A. Ground-truth provenance: [status] — evidence
B. Post-hoc normalization: [status] — evidence
C. Result-file existence: [status] — evidence
D. Dead code: [status] — evidence
E. Scope: [status] — evidence
F. Evaluation type: [label(s)] — evidence
Action items: [specific fixes for WARN/FAIL]
Claim impact: per claim — supported | needs qualifier | unsupported
```

A machine-readable summary with the same fields may accompany it for the
result-to-claim gate.

## How the verdict is used

- The audit is advisory to the pipeline but binding on claim language:
  it never blocks other work, yet its status travels with the results.
- The result-to-claim gate reads the integrity status: `fail` appends an
  integrity concern and caps claim confidence at low; `warn` is flagged;
  no audit run labels downstream verdicts "provisional — no integrity
  audit run".
- A `FAIL` is fixed by repairing the evaluation or narrowing the claim —
  never by re-running the audit until it passes (see the forbidden loop in
  `ccf-common/references/loop-governance.md`).
- Run the audit once per result set. It is verdict-bearing: re-running it
  on a timer adds no signal.
- Honest limit: the audit catches the common patterns above, not every
  possible integrity failure. It is a safety net, not a guarantee.
