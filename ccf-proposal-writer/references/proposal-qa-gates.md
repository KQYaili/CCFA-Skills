# Proposal QA Gates: Four Layers, Scenario Thresholds

> Provenance: protocol adapted from Yuan1z0825/nature-skills,
> `skills/nature-proposal-writer/` (repository Apache License 2.0; the
> source skill's frontmatter additionally declares MIT). Gate order
> and scenario thresholds are carried over; the expert roles are
> mapped to CCFA review roles and the language gate is subordinated
> to ccf-humanization's rules.

## Gate order (content before language)

Run the gates in this order; a later gate never re-opens what an
earlier gate settled, and language work never precedes content work:

1. **Gate 2 — content experts, dispatched by failure mode.** Two
   reviewers matched to the text type and to the observed failure
   mode: for a proposal, a feasibility reviewer and an innovation
   reviewer; for a paper, a methods reviewer and a domain reviewer;
   for a review article, a coverage reviewer and a critical-depth
   reviewer. Findings are graded P0 (blocking), P1 (material), P2
   (minor) and returned as a revision brief, not as rewritten text.
2. **Gate 1 — language scan, detect only.** Flag template-like and
   empty phrasing; do not rewrite at this gate. For English text the
   scan is systematic; for Chinese text it degrades honestly to a
   manual sweep and says so. This gate follows ccf-humanization:
   the goal is direct, evidence-preserving prose, not a detector
   score.
3. **Gate 3 — mechanical validation.** Every claim has a citation or
   an evidence-table entry; methods are described reproducibly;
   numbering of sections, figures, and references is continuous;
   reference insertions or deletions have cascaded renumbering
   correctly.
4. **Gate 4 — scored threshold.** Score on the rubric's dimensions
   (soundness of the research logic, evidence support, feasibility,
   innovation, coherence of the argument map, contract compliance,
   clarity, risk handling), compare the total against the scenario
   threshold, and roll back only the low-scoring dimensions for
   targeted revision — at most 3 rounds (see the stop rules in
   [commitment-lowering-and-stopping.md](commitment-lowering-and-stopping.md)).

## Scenario thresholds

| Scenario | Threshold | Behaviour |
| --- | --- | --- |
| `paper` | 7.0 | Full four-gate run |
| `proposal` | 7.0 | Full four-gate run |
| `internal` | 5.0 | Full run, lower bar for internal reports and briefings |
| `quick` | none | P0 findings only; no scoring |

A score below threshold after the third rollback round is a stop
condition, not a cue for a fourth round of polishing.
