# Reference Metadata Verification (Field-Level)

> Provenance: adapted from Yuan1z0825/nature-skills,
> `skills/nature-ref-verifier/SKILL.md` (Apache License 2.0). The
> field-level comparison matrix, severity levels, confidence labels, and
> batching guidance are carried over; environment-specific tooling notes
> (reference-manager write paths) were generalized to CCFA's
> source-of-truth discipline.

This protocol verifies that a bibliography entry's **metadata** — authors,
title, year, venue, volume/issue, pages, DOI — matches the publisher
record. It answers "is this the right record, transcribed correctly?"

It is distinct from the auditor's other citation work:

- **Context-support verification** (citation-audit mode) answers "does the
  cited source actually support the sentence that cites it?" — a claim
  question, judged against the source's content.
- **Mechanical pre-check** (`scripts/verify-citations.py`) answers "does
  something like this entry exist?" at batch scale, with graded scores.
- **This protocol** sits between them: field-by-field comparison of one
  entry against authoritative records, with a severity and a confidence
  label per entry. Use it for final pre-submission bibliography passes,
  reviewer-flagged citation errors, and migrating a bibliography between
  projects.

Consistent with the rest of the auditor: a source that cannot be reached
makes the entry **Unverifiable**, never "Needs fix" — absence of a record
is not evidence of an error (see the SKIPPED discipline in
`references/citation-verification-rules.md`).

## Step 0: DOI resolvability first (cheapest, highest yield)

For every entry with a DOI, query the DOI record (e.g. Crossref
`/works/<DOI>`) before any other source:

- **404 / unresolvable** → the DOI itself is wrong (likely a mistyped or
  fabricated number). Critical.
- **Resolves** → compare the returned title/authors against the entry.
  A DOI that resolves but points to a *different paper* (misdirection) is
  the single most common serious error class in practice and is invisible
  to existence-only checks. Critical when title or first author differs.

## Step 1: Source strategy

Query in this order, degrading gracefully; use whichever sources the
environment actually provides and record which ones answered:

1. **Crossref** (DOI first, then title+author search) — primary for
   journal/conference papers with DOIs. Coverage caveat: older IEEE
   items and many Chinese journals are absent.
2. **Publisher / venue page** (IEEE Xplore, ACM DL, the journal site) —
   the record of authority when Crossref is missing or stale.
3. **Scholarly web search** (Semantic Scholar, general web search) —
   fallback for entries without DOIs.
4. **CNKI / 万方** — required route for Chinese journals and theses,
   whose DOIs are often not in Crossref.
5. **The local reference library**, if the project keeps one — a fast
   comparison target, but not an authority: a wrong record already in the
   library verifies nothing.

Theses without DOIs are verified on title + author + year + institution
via CNKI/万方/ProQuest-type sources. Manuals, standards, and patents are
not metadata-verified; confirm only that the source is reachable and is
what the citation claims it is.

Early-access drift: for venues with an early-access stage (IEEE and
similar), volume/issue/pages/year change at formal publication. The
current publisher/Crossref record wins; flag the entry Warning (below)
rather than silently rewriting history in older drafts that cited the
early-access version correctly at the time.

## Step 2: Field-level comparison matrix

Compare author names and order, author completeness, title core words,
year, volume, issue, pages/article number, and DOI. Classify every
difference:

### Critical (must fix)

- First author differs, author order changed, or an author is invented.
- An author is **missing** (entry truncates a 5+ author list to the first
  few without "et al." conventions of the target style).
- Pages differ by ≥ 5, or the page range belongs to another article.
- Article number corrupted by look-alike characters (letter read as
  digit: T/7, l/1, O/0 — common in proceedings article numbers).
- Title core words differ (not case/punctuation).
- DOI unresolvable, or DOI resolves to a different paper (Step 0).

### Warning (check suggested)

- Volume year ≠ DOI year (online-first vs issue year).
- Early-access metadata drift (see Step 1).
- Middle initials missing or extra.
- Issue number missing where the record has one.
- Page difference ≤ 4.
- Publisher name in a historical variant.

### Info (no action)

- Title case differences; journal abbreviation vs full name;
  punctuation / "and" vs "&" differences.

## Step 3: Per-item confidence label

Each entry leaves with exactly one label:

| Label | Meaning |
|---|---|
| **Verified** | Authoritative source(s) agree on all compared fields |
| **Check suggested** | Warning-level differences only; human judgment needed |
| **Needs fix** | At least one Critical difference; correct value is known from the record |
| **Unverifiable** | No reachable source could confirm or refute the entry (internal reports, old theses, dead sources) — not an error verdict |

## Step 4: Batching

- Up to ~20 entries: verify serially in one pass.
- More than ~20: split into groups of 10–15 and verify groups in
  parallel (independent subagents or sessions), then merge. Serial
  verification of a full bibliography is an order of magnitude slower
  and adds no accuracy; group boundaries must not split an entry.
- Report counts per label first (Verified / Check suggested / Needs fix /
  Unverifiable), then the Critical table (entry, field, current value,
  correct value, source), then Warnings. Info items are counted, not
  listed, unless asked.

## Step 5: Correction output

- Default output is a **BibTeX patch**: the corrected entries, field by
  field, ready to apply to the project's `.bib` of record.
- Before patching, confirm where the bibliography's source of truth
  actually lives (the `.bib` in the repo, a reference-manager library, a
  generated file). Patch the source of truth, not a downstream copy;
  never edit a generated bibliography file that the next build will
  overwrite.
- A "Needs fix" correction states the value *and the record it came
  from*; a correction without a named source is an opinion, and the
  entry stays Check suggested instead.
