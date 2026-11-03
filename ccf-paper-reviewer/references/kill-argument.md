# Kill Argument: Adversarial Attack–Adjudication Review

Use after standard review rounds have settled, before submission or during
rebuttal preparation, when the question is no longer "what are the
weaknesses?" but "what is the single paragraph that kills this paper?".
Balanced reviews distribute attention across a severity-ranked list and
never quite commit; this exercise forces commitment, then forces an
independent adjudication of the committed attack. It complements the
standard review workflow — it does not replace it.

## Stage 1 — The Attack Memo

An independent cross-model reviewer, in a **fresh context** (no prior
reviews, fix lists, or executor summaries — nothing outside the current
paper files), writes the single strongest argument for rejection:

- Approximately 200 words, hard ceiling 250. One coherent argument, not a
  list: pick the most damaging line of attack and develop it.
- Candidate axes (choose the most damaging combination, do not enumerate
  all): central-claim validity; assumption-vs-claim mismatch (the body
  silently retreats to a narrower object than the title/abstract
  advertise); missing obligations the headline depends on; claim-vs-evidence
  gap (evidence too narrow for the stated breadth); scope overclaim.
- Every accusation cites a specific location (file:line, equation, table).
- No hedging, no acknowledging mitigations. The defense gets the next pass.

**Archive the attack memo verbatim** (in the review report or the task's
handoff record) before Stage 2 begins. An attack that is paraphrased from
memory is no longer the attack that was adjudicated.

## Stage 2 — Independent Adjudication

A second independent reviewer — fresh context again, independent of the
attack thread's history — receives the paper and the verbatim attack memo,
and rules point by point:

1. Decompose the attack into its atomic rejection points (typically 3–7).
2. Classify each point:
   - `answered_by_current_text` — the current source already mitigates it
     (cite the file:line evidence);
   - `partially_answered` — some response exists but does not refute the
     attack as written;
   - `still_unresolved` — the paper has no effective response.
3. For each point record: the attack claim, the verdict, the evidence (or
   its absence), the severity if unresolved (critical / major / minor), and
   one specific actionable fix if unresolved.
4. Close with a net assessment (would the paper survive a senior area-chair
   read of this attack?) and at most three top action items.

Two classification disciplines: an **author-chosen position** (deliberate
title scope, deliberate omission) is `partially_answered` with a note that
the position is intentional, plus a judgment of whether it is sustainable
under the attack — never auto-graded `answered_by_current_text` merely
because it is intentional. And the adjudicator must not minimize: an honest
`still_unresolved` is the valuable output.

## Verdict (computed, never self-graded)

The adjudicator emits per-point classifications only; the top-level verdict
is computed from the counts by this fixed mapping:

| Verdict | Condition |
| --- | --- |
| FAIL | ≥1 `still_unresolved` at critical severity |
| WARN | ≥1 `still_unresolved` at major/minor severity, or 0 unresolved with ≥1 `partially_answered` at critical/major |
| PASS | 0 `still_unresolved`, and any `partially_answered` points are all minor (or none) |

Run this **once** per stable draft — the attack changes only when the paper
changes, so re-running it on a timer or in a loop adds no signal. Detect-only
by default: it never edits the paper; fixes are the author's (or the
writer's, under instruction) to apply. It is most valuable for papers whose
headline depends on a few load-bearing claims (theory papers, scope-heavy
empirical claims); for an early draft whose headline is still moving, fix
the headline first.

> Provenance: adapted from wanshuiyin/Auto-claude-code-research-in-sleep
> (ARIS, MIT License), `skills/kill-argument/SKILL.md`, batch-2 integration
> 2026-11-03. Backend-specific reviewer routing, model names, trace/HTML
> machinery, and the ARIS audit-artifact schema were dropped; the reviewer
> is any independent cross-model reviewer in a fresh context, matching this
> repo's reviewer conventions.
