# Bibliographic Integrity Signals

Use when auditing a bibliography for a different class of problem than
transcription accuracy or claim support: whether a cited work's *status*
has changed, whether its text carries paper-mill risk markers, and whether
an existence check actually resolved. This is a protocol only — it produces
advisory signal rows with recorded provenance, never verdicts about a work's
legitimacy.

## Signal 1 — Publication Status (Retraction / Correction / Concern)

- Sources: OpenAlex (`is_retracted`) and Crossref update metadata — an
  `updated-by` event on the cited work, or an `update-to` event on a notice
  pointing at it. A DOI is required; title-only status matching is not
  permitted (a manual entry without a DOI is recorded `not_checked`).
- Reduction: the latest *dated* retraction/reinstatement event wins.
  Conflicting undated events reduce to `disputed`. Disagreement between
  OpenAlex and Crossref is reported explicitly, never averaged away.
  Missing or degraded data is `unresolved` — it is never silently read as
  clean.
- Freshness: a status observation is stamped with its check time; treat
  observations older than ~30 days as `stale` and revalidate before any
  consequential use.
- **Boundary:** report the status and its source, nothing more. This signal
  does not decide that a paper's findings are unsound, that citing it is
  illegitimate, or that a manuscript is unpublishable. A legitimate-use
  exception (e.g. citing a retracted work *about* its retraction) requires
  an explicit author declaration plus a citation of the retraction notice
  itself; the check does not judge whether the prose truly discusses it.

## Signal 2 — Phrase-List Screening (Tortured Phrases)

- A deterministic phrase-pattern matcher screens title and abstract text
  against a curated list of known paper-mill paraphrase artifacts.
- Epistemic class: **heuristic advisory**. A match is worded exactly as
  "phrase-list match requiring review". A zero-match result says only "no
  phrase-list match observed on the checked surface" — absence is not a
  clean certification.
- **Fail-closed surfacing:** each (citation, surface) pair yields a row —
  `detected`, `no_match`, or `not_checked`. A surface that could not be
  screened is reported `not_checked`, never silently passed.
- No output may call a work contaminated, generated, fraudulent, or
  paper-mill-produced, and the matcher never suggests replacement text or
  edits the manuscript. Contextual judgment, if wanted, is a separate,
  explicitly labelled step by a human or model reviewer.

## Signal 3 — Existence Tri-State

An existence check resolves to exactly one of three states:

- `confirmed` — a matching record was retrieved (title + authors agree).
- `not_found` — a genuine search over the declared sources returned nothing;
  only this state supports calling a reference fabricated, and only together
  with the search record.
- `undetermined` — the check could not decide: no identifier, an identifier
  that resolves to a *different* work, a degraded API response, or partial
  metadata. **An identifier mismatch is `undetermined`, never `not_found`** —
  a wrong DOI in a bibliography is a transcription defect (route it to
  [ref-metadata-verification.md](ref-metadata-verification.md)), not proof
  that the cited work does not exist.

## Relation To The Other Citation Layers

- [citation-verification-rules.md](citation-verification-rules.md) +
  `scripts/verify-citations.py`: mechanical existence/metadata pre-check
  grading (batch 1). This protocol's tri-state governs how its outcomes may
  be *worded*.
- [ref-metadata-verification.md](ref-metadata-verification.md): field-level
  transcription correctness.
- This file: status, phrase-risk, and existence-semantics signals. None of
  the three layers judges whether a source *supports* the claim citing it;
  that remains the auditor's context-support check.

> Provenance: independently worded protocol adaptation of the bibliographic
> integrity signal designs in Imbad0202/academic-research-skills (CC BY-NC
> 4.0 — principles only, no code or text copied), batch-2 integration
> 2026-11-03. Upstream resolver/screening code was not imported.
