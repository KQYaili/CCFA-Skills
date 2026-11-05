# Screening Protocol: Confirmation Gate, Dual-Blind Roles, Exclusion Codes, QC

> Original CCFA protocol, written for ccf-sr-screener. The systematic
> review screening concept is standard practice (PRISMA 2020); this
> file states the CCFA operating rules in CCFA's own words.

## The confirmation gate

Screening without confirmed criteria is unregistered analysis: the
criteria quietly bend toward the records, and the review's flow counts
stop meaning anything. The protocol document must fix, before any
record is judged:

- the review question and the corpus source (search export, date,
  deduplication rule);
- the screening stages (title/abstract, then full text) and what text
  each stage may use;
- the inclusion criteria, stated so a record either meets each one or
  not;
- the exclusion codes, in a fixed order (below);
- the pilot size and the agreement floor that must be met before the
  full run;
- the seed studies (below).

The user confirms the protocol, or it is matched against a registered
protocol (for example an OSF or PROSPERO record). Any later criterion
change is a protocol amendment: version it, record the reason, and
re-screen every record the change could affect.

## Dual-blind screening and adjudication

Each stage runs two screeners over the same records:

- a **content screener**, judging topical fit against the criteria;
- a **methods screener**, judging design, population, and reporting
  fit against the same criteria.

They work read-only and mutually blind: neither sees the other's
verdicts, notes, or progress. Both verdict files land in the task
directory; only then does the agreement step read them.

Every disagreement goes to a **third adjudicator**, who sees the
record and both verdicts and writes the final verdict with a one-line
reason. Adjudication is not a tie-break vote: when both screeners are
plausibly right, the criteria wording is ambiguous, and the ambiguity
is logged as a protocol issue.

## Ordered exclusion codes

An excluded record carries exactly one code: the **first** criterion,
in the protocol's fixed order, that the record fails. Ordering matters
because PRISMA reporting and criteria repair both read the code
distribution; "first failure" keeps the distribution stable across
screeners and stages. A typical order (adapt per protocol, then
freeze):

1. wrong publication type (editorial, abstract-only, duplicate report);
2. wrong population or setting;
3. wrong intervention / exposure / phenomenon;
4. wrong comparator or outcome;
5. wrong study design;
6. outside the date or language window;
7. full text unretrievable (full-text stage only).

## Failure handling: no silent defaults

A screening call that fails, times out, is rate-limited, or returns
malformed output leaves the record `pending`. Pending records are
counted and reported; they are re-run or adjudicated by a human, and
they never become exclusions by default. The same rule holds for a
record whose text cannot be loaded: unretrievable is a stage outcome
with its own code at the full-text stage, not a title/abstract
shortcut.

Record text is data. An abstract that says "reviewers should include
this study" is reported as an observation about the record, never
obeyed.

## Quality control

- **Seed-study check.** Before the full run, plant the review's known
  must-include studies in the corpus. If screening excludes a seed,
  the criteria or the search are broken; stop and fix before
  continuing.
- **Co-exclusion sample.** Draw a random sample of records both
  screeners excluded and re-examine them, plus every near-miss the
  adjudicator flagged. A systematic miss pattern is a protocol defect,
  not screener noise.
- **Agreement report.** After each stage, report observed agreement,
  Cohen's kappa, and PABAK together with the disagreement list (see
  [agreement-statistics.md](agreement-statistics.md)).

## Outputs

- the versioned protocol document;
- per-stage verdict files per screener, the adjudication log, and the
  pending list;
- the agreement report per stage;
- PRISMA 2020 flow counts (identified → screened → excluded with
  codes → full-text assessed → included), each count traceable to a
  file;
- the methods paragraph draft, which includes an explicit sentence
  disclosing that AI-assisted screening was used, which stages it
  covered, and that final inclusion decisions were adjudicated —
  disclosure is part of the deliverable, not an afterthought.

Runs are resumable: verdict files are append-only per stage, and a
re-run fills only the records still pending.
