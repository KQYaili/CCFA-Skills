# Citation Verdict Protocol For Search Reports

Use when a literature search produces candidate references that downstream
work (idea review, writing, rebuttal) may rely on. Every candidate leaves
the search with one of five verdicts; the verdict, not the searcher's
confidence, decides how the reference may be used.

## Two-Step Verification

1. **Existence.** Look up the full title (or a distinctive fragment plus the
   first author's surname). A hit must match on title *and* authors; a hit
   with a different title or author list is a different work until confirmed
   otherwise. No hit after a genuine search means the reference does not
   enter the report as a citation at all.
2. **Claim accuracy.** Check that the finding attributed to the paper is
   actually supported by its title, abstract, or the inspected passage.
   Metadata alone never licenses invented method details or numbers.

## The Five Verdicts

| Verdict | Meaning | Permitted use |
| --- | --- | --- |
| `VERIFIED` | Exists; the attributed finding matches the source | Usable as cited |
| `MINOR` | Exists; small wording drift in the attribution | Usable after correcting the wording |
| `MAJOR` | Exists; the attribution misrepresents it | Not usable as cited; correct the claim or drop the reference |
| `UNVERIFIABLE` | Existence cannot be confirmed | Not usable; excluded from the survey |
| `PAYWALL` | Exists; accessible metadata is insufficient for the attributed claim | Metadata-level statements only (identity, venue, year) |

## Grey Zone Means Unused

An unconfirmable citation stays out — it is never kept with a warning label
attached. "There is probably a paper showing X" without a retrieval hit is
not a citation. One fewer reference always beats one invented reference. In
a search *report* (a working document addressed to the researcher), mark the
gap explicitly, e.g. `[unconfirmed: no work retrieved in this direction]`.
That marker convention belongs to reports only; manuscript prose follows
the paper writer's rules and admits no such markers.

## Invented-Citation Signals And Cascade Recheck

Treat a candidate as suspect when: its title matches the point being argued
suspiciously perfectly; the author–title–year–venue combination returns
zero retrieval hits; or one author appears many times in the candidate list
but only once in retrieval.

On confirming an invented citation: remove it immediately, then **re-examine
every judgment that depended on it** — screening tiers, novelty and overlap
assessments, and any claim whose support cited it. The cascade is not
optional: a fabricated source invalidates the reasoning built on it, not
just the bibliography entry. Record which dependent judgments were re-checked
and what changed.

> Provenance: independently worded adaptation of the citation-verification
> protocol in HKUSTDial/Supervisor-Skills, `skills/deep-research/references/citation-protocol.md`
> (mixed CC BY / skill-specific licensing; principles only, no prose copied),
> batch-2 integration 2026-11-03. The five-verdict vocabulary and cascade
> rule are the increment; existence/support checking machinery itself lives
> with `ccf-integrity-auditor`.
