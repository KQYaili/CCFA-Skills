# Loop Governance: Acceptance Gates for Autonomous Iteration

> Provenance: adapted from wanshuiyin/Auto-claude-code-research-in-sleep
> (ARIS), `skills/shared-references/acceptance-gate.md`,
> `skills/auto-paper-improvement-loop/SKILL.md` (Edit Whitelist), and
> `skills/integrity-forensics/SKILL.md` (the One Forbidden Loop)
> (MIT License, Copyright (c) 2026 wanshuiyin). Vendor backend names and
> ARIS skill names were replaced with CCFA roles and gates; the taxonomy
> and detectors are carried over.

Any CCFA workflow that keeps working until a condition is met — an
autonomous research loop, an auto-revision loop, a retry/debug cycle —
terminates on a gate it evaluates each round: "are we done yet?" That
gate is where self-acquittal sneaks in. The loop body may be one model
family throughout; the **gate** is what this contract governs.

One line, and the whole contract in seven words:

> **A loop can DRIVE; it cannot ACQUIT.**

The loop may freely *drive* itself toward a target — schedule the next
configuration, recompile, re-run the failed job, fan out search branches.
What it may not do is *acquit* its own work — declare the paper good, the
proof valid, the claim supported, the idea novel, the review satisfied.
Acquittal is a cross-model act.

## The two gate types

Classify **every** stop/accept gate of a loop as exactly one of these.
There is no third bucket; if a gate seems to be both, it is two gates —
split it (see "Compound gates").

### Type-A — execution / objective gate

A machine-checkable or externally observable signal of *what happened*,
with no judgment of *merit*. The executing agent **may** judge Type-A
gates itself — it is execution bookkeeping, not a verdict. A gate is
Type-A iff a non-LLM process (an exit code, a file stat, a counter, a
parser reading a harness's own output) could in principle give the same
answer.

- exit code == 0; the PDF compiled; `figures/result.png` exists;
- N/N jobs finished; the test suite passed; no NaN in the loss log;
  training reached `max_steps`;
- the reviewer **was invoked** and a verdict artifact exists;
- every checklist item was **attempted**;
- a budget counter (rounds, patience, wall-clock, compute) hit its bound;
- the benchmark harness emitted a number and it parsed.

Self-judging "did the audit run?" is fine. Self-judging "did the audit
*pass*?" is not — that is Type-B.

### Type-B — quality / correctness / acceptance gate

A judgment of *merit, correctness, or sufficiency*. The executing agent
must **never** judge a Type-B gate on its own work — it requires an
**independent cross-model reviewer**: a different model family, fresh
context, reading the artifacts directly (paths, not the executor's
summaries).

- "the paper is submission-ready" / "the proof is valid" / "the gap is
  closed";
- "the claim is supported by the results" (CCFA instance: the
  result-to-claim gate);
- "the evaluation is honest" (CCFA instance: the experiment audit);
- "the idea is novel" / "the review is satisfied" / "the weaknesses are
  addressed";
- "score ≥ X" — when the executing model family assigned the score;
- "this configuration is good enough to publish" / "the rebuttal answers
  the reviewer" / "the fix is correct" (as opposed to "the fix made the
  test pass" — Type-A).

A hundred rounds of the same family judging itself is still one model
family. Iteration count does not launder a verdict.

### The dividing question

> *Could a dumb script with no taste answer this gate?*
>
> **Yes → Type-A** (self-judgment is bookkeeping).
> **No — it needs taste, correctness, or domain judgment → Type-B**
> (route it to a different model family).

### Compound gates: split, don't average

Natural-language stop conditions bundle A-parts and B-parts. "Stop when
the paper is submission-ready" decomposes into, e.g.: A — all audits were
invoked and emitted their artifacts; A — the validation scripts exit 0;
B — "the paper is actually good enough to submit" → cross-model verdict.
Never collapse a compound gate to its A-part and call the loop safe; the
B-part does not disappear because it is inconvenient — it gets routed.

## Decision procedure for any new loop

1. **Enumerate every stop/accept gate** — the headline condition, the
   convergence early-exit, the patience bail-out, the per-round "is this
   round done?" check, the final "are we finished?" check.
2. **Classify each A or B** with the dividing question; split compound
   gates and classify the parts.
3. **Type-A:** self-judgment allowed; prefer an external check (exit
   code, stat, counter) over an "I believe it finished" wherever one
   exists.
4. **Type-B:** route to an independent cross-model verdict. The loop
   continues or stops on *that* verdict, not on the executor's reading
   of it. Save the verdict as an artifact a third party can inspect.
   If no independent reviewer is reachable, the gate reports
   `REVIEW_UNAVAILABLE` and the loop may keep driving or pause — it may
   not acquit.
5. **State the provenance in the skill or plan**: one line per
   terminating condition naming its type and who signs off.
6. **Refuse the anti-pattern**: a loop whose continue/stop decision reads
   a quality verdict produced by the same model family that did the
   work. Test: if removing the cross-model reviewer would still let the
   loop decide to stop-accept, the loop is self-acquitting.

Objective-metric loops (design-space search, hyperparameter sweeps) are
Type-A all the way down *as search*: "configuration B beats A on the
harness's own number" is a parser's fact. Two adjacent judgments are
Type-B and must leave the loop: "this configuration is good enough to
publish" (sufficiency) and "this benchmark is the right thing to
optimize / the result generalizes" (framing). The loop may self-terminate
on "best found within budget"; the publishable claim goes through the
result-to-claim gate.

## Fan-out is not a jury

Same-family fan-out is fine for Type-A coverage — ten branches each
attempting a different search, unioning hits; N drafters each producing
a section, with an "all sections drafted" completion check. It is never
a Type-B jury: N reviewers from the *same* family scoring a paper and
averaging is correlated blindness wearing a jury costume — their
agreement evidences shared priors, not correctness. A Type-B verdict
needs a different family, not a bigger N of the same one. Fan-out scales
breadth and coverage; the acquittal always funnels to the one
cross-family verdict.

## Edit whitelist for automated revision loops

A loop that applies reviewer-driven edits to a manuscript (auto-revision,
resubmit microedits, camera-ready fixes) takes an optional edit whitelist
so structural constraints are enforceable parameters, not things the
model is asked to remember. Default off; when set, it is loaded before
the first edit round and a load failure aborts the loop rather than
proceeding unconstrained.

```yaml
allowed_paths:        # empty = all paths allowed
  - sec/*.tex
forbidden_paths:      # always wins over allowed_paths on overlap
  - "**/*.bib"
  - "**/*.sty"
forbidden_operations: # checked against ADDED lines of each edit's diff
  - new_cite
  - new_bibitem
  - new_theorem_env
  - numerical_claim
forbidden_deletions:  # checked against REMOVED lines
  - delete_existing_cite
  - delete_theorem_env
max_edits_per_round: 30
rationale: "Resubmit mode: text-only microedits; structure frozen."
```

Forbidden-operation detectors (added lines only; deletions exempt):

| Operation | Detector |
|---|---|
| `new_cite` | `\\cite[a-zA-Z]*\{[^}]+\}` (cite, citep, citet, citeauthor, …) |
| `new_bibitem` | `\\bibitem\{[^}]+\}` |
| `new_theorem_env` | `\\begin\{(theorem\|lemma\|proposition\|corollary)\*?\}` |
| `numerical_claim` | a numeric token `\b\d+(\.\d+)?%?\b` in added lines that does not appear in the replaced/deleted lines — genuinely new numbers, not edits to existing ones |

Before each edit: resolve the target path → path check → operation check
on the diff. A rejected edit is logged (file, reason `path`/`operation`,
offending pattern, the reviewer concern that motivated it) and the round
continues — a rejection never aborts the round, and rejected edits are
never silently dropped. The `rationale` is echoed into the loop's log so
the audit trail records why edits were constrained. Without a whitelist,
a revision loop is free to add citations, theorem environments, and
numerical claims; in resubmit/camera-ready modes, where the structure is
frozen by external constraint, that freedom is exactly what must be
removed.

## The One Forbidden Loop

**Never run "edit → re-scan → repeat until CLEAN".** That objective
teaches the editor to defeat the detector — deleting an anchored span
kills a flag faster than fixing the number — and produces a paper
laundered against its own audit. After fixes, a re-scan exists to confirm
the *discrepancy* is gone and to catch new ones; the findings ledger, not
the scanner's verdict, decides whether a gate opens. A scanner's clean
result means "no flag found in the evidence at hand" — it is never an
acquittal, and no loop may treat it as one.

## Epistemic status of a cross-model PASS

A cross-model PASS is a heterogeneous second opinion, not ground truth:
a differently built model, reading the artifact cold, did not find the
flaw the author would miss. It does not mean the work is correct, novel,
or publishable. It is the strongest automatable quality check this
framework has — and the human stays in the loop for what no in-framework
verdict supplies: current literature, venue taste, and ground truth. A
green gate lowers risk; it does not transfer accountability.

## Where CCFA already applies this

- `research-rigor-gates.md`: kill gates and confirmatory/exploratory
  separation — the experiment-side instance (a preregistered kill gate
  is a pre-committed Type-B decision, made before results exist).
- `ccf-integrity-auditor/references/result-to-claim-gate.md`: Type-B,
  cross-model by construction.
- `ccf-experiment-designer/references/experiment-audit.md`: Type-B.
- The validation suite (`ccf-common/scripts/check_*.py`, test scripts):
  Type-A — the executor reads exit codes, it does not grade them.
