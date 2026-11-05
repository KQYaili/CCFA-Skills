# Citation Crosscheck: Dual-Blind Reconstruction of a Reference List

> Provenance: protocol adapted from wanshuiyin/Auto-claude-code-
> research-in-sleep (ARIS), `skills/citation-crosscheck/SKILL.md`
> (MIT License, Copyright (c) 2026 wanshuiyin), condensed and
> reworded into CCFA conventions. Backend names from the source are
> replaced with CCFA roles: the two extractors are independent
> subagent runs, and verdicts are assigned by the integrating owner.

## Position in the auditor's citation stack

This is the **deep mode** of citation checking, beyond the two
shallower layers already in this skill:

- the batch-1 citation scripts give a mechanical existence and field
  pre-check over the `.bib`;
- [bibliographic-integrity-signals.md](bibliographic-integrity-signals.md)
  (batch 2) reads integrity signals — retraction status, tortured
  phrases, existence tri-state semantics.

Crosscheck answers a different question: not "does this entry look
plausible" but "does an independent reconstruction, built without
seeing the entry, agree with it field by field". Run it when the
bibliography changes materially (submission, camera-ready, rebuttal
evidence), not on every edit.

## Why blind

A single reviewer who reads the `.bib` first anchors on it: wrong
years, dropped authors, and transposed venues all "look correct"
because the entry itself supplies the expectation. The crosscheck
removes the anchor by construction — extractor B never sees the
entry it is checking.

## Procedure

1. **Extractor A — verbatim from the source.** Extract every entry
   from the local `.bib` exactly as written: authors in order, year,
   venue, DOI / arXiv ID, pages. No normalization, no silent fixes.
2. **Extractor B — blind reconstruction from the web.** Given only
   the entry's **title and first author** (plus an opaque, run-local
   deduplication key), reconstruct the bibliographic record from
   authoritative sources: arXiv, DBLP, Crossref, the ACL Anthology,
   and official proceedings (NeurIPS / PMLR / OpenReview). B must not
   read the `.bib` or any repository file; web sources only.
3. **Mechanical field diff.** Compare A and B field by field and emit
   the delta: dropped or re-ordered authors, year mismatch, venue
   mismatch, DOI that does not resolve, arXiv ID mismatch, page
   drift.
4. **Verdicts by the owner only.** The integrating owner assigns
   `MATCH`, `MINOR`, or `MISMATCH` from the delta; extractor shards
   never assign verdicts. Preprint-vs-published differences and
   cosmetic formatting drift are `MINOR` — reported, never silently
   upgraded to `MISMATCH`, and never silently "repaired" either.
5. **NEEDS_WEBCHECK.** Entries that legitimately live outside the
   indexed sources (blog posts, technical reports, software) are
   marked `NEEDS_WEBCHECK` rather than flagged as fabricated; a
   missing record is a triage state, not a verdict.

## Boundaries

- Scope is bibliographic existence and field accuracy only. Whether
  a correctly-listed reference actually supports the sentence citing
  it is context-fit, and belongs to the auditor's context-support
  checks, not to this protocol.
- This protocol is verdict-bearing. **Never wrap it in a loop, a
  schedule, or a cron**: it runs once per bibliography change, with
  a human reading the verdict table.
- Fixes to the `.bib` follow from the verdicts and are applied by the
  owner with the delta attached; extractor B's record is evidence,
  not an auto-merge source.
