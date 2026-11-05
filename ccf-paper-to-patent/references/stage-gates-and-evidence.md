# Stage Gates and Evidence Rules for Paper-to-Patent Conversion

> Provenance: protocol adapted from Yuan1z0825/nature-skills,
> `skills/nature-paper-to-patent/` (Apache License 2.0). The stage
> sequence, source-ID scheme, and support-state vocabulary are
> carried over and condensed into CCFA wording; the two deterministic
> validators are imported in `../scripts/` under the same license.

## Stage gates

- **Stage 0 — intake and risk flags.** Confirm jurisdiction (default:
  CNIPA-oriented Chinese drafting), source completeness, and red
  flags: already-published material whose dates matter, third-party
  content mixed into the source, missing inventor facts. Flags are
  recorded, never resolved by inference.
- **Stage 1 — source map.** Split the source into stable blocks and
  assign IDs: `P001…` text blocks, `E001…` equations, `F001…`
  figures, `C001…` code or supplementary evidence. Every later
  artifact cites these IDs; a renumbering invalidates downstream
  mappings and must cascade.
- **Stage 2 — technical inventories.** Terminology ledger (one
  canonical Chinese term per technical object; aliases recorded and
  then barred from formal text), input–operation–output map of the
  method, formula inventory (each equation kept, simplified, or
  dropped, with a reason), figure inventory, and an
  implementation-gap list (details a skilled reader would need that
  the source does not give).
- **Stage 3 — evidence ledger.** Every material claim feature is
  mapped to source IDs with a support state:
  - `explicit` — the source states the feature directly;
  - `inherent` — the feature is necessarily present in what the
    source describes;
  - `needs-confirmation` — plausibly present but not established;
  - `unsupported` — no source basis.

  Gate rule: drafting may not start while an essential feature is
  `unsupported`, and every `needs-confirmation` feature must either
  become an inventor question or be removed from the claim plan.
- **Drafting.** Claims first; specification, figures, embodiments,
  and abstract follow the claim terminology and step order exactly.
  The principal flowchart is built from the main method claim's
  ordered steps, and its final node names a concrete domain output.

## Support-state discipline

- `unsupported` features are barred from formal claims — no
  exceptions for features that "should" work.
- `[TO CONFIRM: …]` markers live in inventor-question lists and draft
  annotations, never inside formal claim text.
- Inventorship, ownership, dates, and prior-art status are never
  inferred from the source; missing values stay missing.

## Validation semantics

`../scripts/validate_patent_draft.py` checks the structured draft:
required sections, claim numbering continuity, source-ID validity
and duplicates, terminology-ledger consistency (no duplicate or empty
canonical terms, no forbidden aliases in formal text), evidence-ledger
support states and source links, feature-mapping completeness, and
formula-inventory dispositions. `../scripts/audit_claims.py` checks
the claims text itself: numbering, dependency references, undefined
introduced terms, leftover placeholders.

Delivery semantics are strict: any ERROR finding blocks delivery as a
finished draft, and quality scores below the validator's thresholds
force the package to be labelled an **incomplete draft** with the
failing dimensions listed. Passing the scripts is a structural floor,
not a quality or patentability judgement.
