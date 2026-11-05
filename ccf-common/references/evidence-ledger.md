# Typed Evidence Ledger (Opt-In)

> Provenance: protocol adapted from WUBING2023/PaperSpine,
> `src/skill/references/scientific-evidence-ledger.md` (MIT License,
> Copyright (c) 2026 PaperSpine contributors), reworded into CCFA
> conventions. The deterministic checker is imported at
> `../scripts/scientific_evidence_check.py`.

## Status: opt-in, never a mandatory database

This ledger is an **optional structured backing** for a manuscript
that explicitly adopts it. It is not a required registry and it does
not replace [claim-promotion-gate.md](claim-promotion-gate.md): the
promotion gate deliberately works on the artifacts a project already
has, and most manuscripts should keep doing exactly that. Adopt the
ledger when a manuscript's claims, numbers, and results have grown
past what prose notes can keep consistent — and record the adoption
in the manuscript's own workfiles, not here.

## The ledger file

One JSON file per adopting manuscript:
`scientific_evidence_ledger.json` in the manuscript's task directory.
The six record groups sit under a top-level `records` object, next to
the ledger-level `status`. Every record ID is its group prefix plus
at least three digits (for example `S001`, `C042`):

| Group | Prefix | Holds |
| --- | --- | --- |
| `sources` | `S` | Evidence sources: papers, datasets, run records |
| `claims` | `C` | Manuscript claims, each with its `text` and its `boundary` |
| `numeric_facts` | `N` | Numbers as their own class — a value with its unit, condition, and provenance, separate from the prose claims that quote it |
| `methods` | `M` | Methods and configurations that produced results |
| `outcomes` | `O` | Outcome variables and metrics as defined |
| `results` | `R` | Result records linking claims, methods, and outcomes, with `conditions` and `uncertainty` stated |

Sources, claims, methods, outcomes, and results must each contain at
least one record; numeric facts may be empty when a manuscript has
none. Duplicate IDs are rejected, and every cross-reference
(`source_ids`, `claim_ids`, `numeric_fact_ids`, `method_ids`,
`outcome_ids`, `result_ids`) must resolve to an existing record of
the right prefix class.

## State machine

Each record carries a `verification_state`:

- planning phase allows `planned` and `unverified` alongside the
  final states;
- final states are `verified` (requires a `verified_by` note),
  `user_authoritative` (requires an `evidence_locator`), and
  `not_applicable`.

Sources, numeric facts, methods, and results must declare the field;
claims and outcomes may omit it but are validated when they carry
one.

Claims link to sources or results — a claim with neither is not
promotable, ledger or no ledger. At final phase, a claim marked
`used_in_final: true` must carry `result_ids`, and the ledger's
`status` must be `manuscript_ready`.

## Checking

```text
python <ccf-common>/scripts/scientific_evidence_check.py <output_dir> [--phase planning|final] [--markdown] [--json] [--write]
```

The checker validates structure, ID classes, cross-references, and
state requirements, and exits non-zero on failure. It checks that
the ledger is *consistent*, never that its contents are *true* —
verification of the underlying evidence stays with the owners named
in `verified_by`.
