# Primary-Source Claim Trace (Scoped)

Owner: \`ccf-integrity-auditor\`. Use when a conclusion, novelty claim, paraphrase or cited fact relies on a **secondary account**, ambiguous bibliography entry, or a source whose actual support is unclear. This supplements existing [ref-metadata-verification.md](ref-metadata-verification.md), [citation-crosscheck.md](citation-crosscheck.md) and the result-to-claim gate; it does not replace those checks or require a separate report for routine editing.

## Separate the four questions

1. **Identity:** does the cited work / record really exist, and which version?
2. **Provenance:** is the cited item an original study, official dataset / protocol, review, press account, repository copy or model recollection?
3. **Support:** does an *inspected passage, equation, method or result* say what the draft claims, with the same assumptions and scope?
4. **Current status:** has an official correction, retraction, superseding version, or material follow-up changed this assertion?

A bibliographic match is evidence for (1), not (3). Reaching an original PDF is evidence for (2), not proof of the draft's claim. A formally published but corrected paper is not automatically invalid, but the correction must be considered for dependent statements.

## Trace only what matters

- Extract the exact **claim–source pairs** for the requested scope; one sentence may contain two distinct claims supported by different sources.
- Read the provided or cited original first; when the citation is to a secondary summary, follow its original-work references to the publisher, official repository, ACL Anthology, arXiv version, OpenReview proceedings, dataset documentation or actual experiment record.
- Use abstract/metadata only for identity and preliminary screening. If a mechanistic, empirical, directional or negative claim depends on the method/results, read the relevant full section or mark support unresolved.
- Capture the claim in the author's words and the *smallest recoverable source anchor*: page / section / equation / table / figure / record path and source version. Keep excerpts brief; do not paste the full paper into the audit.
- For recency-sensitive claims, check official correction/retraction/version information. State the check date. When live tools or the source are unavailable, report it; do not invent a fresh status.
- Distinguish **no source found** from **source contradicts claim**. A negative priority claim ("first", "only", "no prior work") is bounded by actual search coverage and is rarely verifiable exhaustively.

## Verdict grammar (per pair)

| Verdict | Meaning | Minimal repair |
| --- | --- | --- |
| \`SUPPORTED\` | Original inspected passage supports the claim within its stated conditions | Preserve the claim and anchor |
| \`NARROWER\` | Source supports a weaker or more conditional version | Limit subjects, population, quantity, setting or tense |
| \`CONTRADICTED\` | Inspected primary source conflicts with the wording / direction / number | Correct or withdraw after checking original result |
| \`METADATA_ONLY\` | Citation exists but needed body text was not read | Do not promote its content to verified |
| \`UNRESOLVED\` | Source, version, accessibility or claim mapping remains unsettled | Name the missing passage or other source |
| \`OUTDATED\` | A dated correction / later version materially changes the claim | Cite the current version and amend interpretation |

Use \`NOT_APPLICABLE\` only for a non-factual stylistic proposition. \`SUPPORTED\` applies to the **specific inspected claim–source pair**, not the whole paper or downstream derivations.

## Output and boundaries

Default internal handoff: \`claim_id | manuscript location | source URL/version | inspected passage location | source tier | verdict | minimum edit | unresolved dependency\`. If the user asked for an audit, fold the findings into the existing auditor report instead of making a new report type.

No source replacement, bibliography mutation, or manuscript edit without appropriate authorization. Keep user-provided unpublished materials private. The source-of-truth for experimental numbers remains original result records; a citation trace must not silently substitute public paper statistics for a project's own runs.

## Source and licensing note

Independent CCFA adaptation of primary-source chasing and claim–source separation motivated by [The Researcher](https://github.com/rohankgeorge/the-researcher) (MIT). It does not import code or claim to verify truth beyond the inspected evidence.
