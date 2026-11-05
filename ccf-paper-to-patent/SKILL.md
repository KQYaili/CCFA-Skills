---
name: ccf-paper-to-patent
description: "Convert a paper, technical report, or project documentation into a Chinese patent application draft with source-mapped evidence and stage gates. Use for 专利申请, 论文转专利, 权利要求书撰写, 技术交底书, and paper-to-patent conversion. Every claim feature must trace to a stable source ID; unsupported features are barred from claims. This skill produces drafting aids, not patentability opinions."
metadata:
  ccf_skill_controls:
    handoff_question_mode: partial
    respect_session_denylists: true
    protect_idea_scope_in_writing: true
    private_material_safety: moderate
    shared_controls: ../ccf-common/references/
---

# CCF Paper To Patent

## Family File Contract

Before file work, reuse canonical paths and one task/artifact working directory; default to project-root `ccfa-workfiles/<purpose>/<artifact-id>/`. Update in place, preserve inputs, and use UTF-8 with Chinese-text checks. Apply [artifact-contracts.md](../ccf-common/references/artifact-contracts.md) for naming, ownership, and task-created cleanup; handoffs inherit these paths.

## Collaboration Contract

Before specialist execution, read and apply [ccf-humanization](../ccf-humanization/SKILL.md) first, then [ccf-common](../ccf-common/SKILL.md). At every handoff, reuse their applicable active rules or refresh missing/changed ones. Both preflights are required even without prose; detailed editing, experiment, and maintenance modes run only when relevant.

Integrate necessary specialist contributions under one owner; reuse valid prerequisites and verify affected results. Follow the [cooperation routes](../ccf-common/references/routing.md) without duplicate reports.

## Disclaimer

This skill is a drafting aid. Its output is **not** a patentability opinion, an infringement opinion, a freedom-to-operate assessment, or a guarantee that an application will be granted. Prior-art conclusions, inventorship, ownership, and filing strategy require a qualified patent professional; the skill never infers them from source material.

## Core Rule

Nothing enters a claim without evidence. Before drafting, assign stable source IDs to the source material — `P001…` for text blocks, `E001…` for equations, `F001…` for figures, `C001…` for code or supplementary evidence — and map every material claim feature to the IDs that support it, with a support state of `explicit`, `inherent`, `needs-confirmation`, or `unsupported`. A feature whose support is `unsupported` is barred from formal claims. Never infer inventorship, ownership, unpublished implementation details, publication dates, or prior-art conclusions; unresolved points become `[TO CONFIRM: …]` questions for the inventor, placed outside the formal claims.

## Modes

- `full-draft`: paper or report → source map, inventories, evidence ledger, then 权利要求书 / 说明书 / 说明书摘要 / 摘要附图.
- `claims-only`: draft and audit the claims set against an existing evidence ledger.
- `disclosure`: produce a 技术交底书 (technical disclosure) for handover to a patent agent instead of a filing draft.
- `audit`: run the deterministic validators over an existing draft package without redrafting.

## Workflow

1. Run the stage gates in order (see [stage-gates-and-evidence.md](references/stage-gates-and-evidence.md)): intake and risk flags → source map → technical inventories (terminology ledger with one canonical Chinese term per object, input–operation–output map, formula inventory, figure inventory, implementation-gap list) → evidence ledger. The ledger gate is hard: no essential feature may remain `unsupported`, and every `needs-confirmation` feature becomes an inventor question or is removed.
2. Draft claims first, then the specification, figures, embodiments, and abstract aligned to the claim terminology and step order. The main flowchart is generated from the principal method claim's ordered steps; its final node must name a concrete domain output, not a generic "result".
3. Keep the structured draft data in the documented schema (see [draft-schema.md](references/draft-schema.md)) so the validators can check it; formulas follow the OMML handling note (see [formulas-to-omml.md](references/formulas-to-omml.md)).
4. Validate before delivery: run `scripts/validate_patent_draft.py` over the draft JSON and `scripts/audit_claims.py` over the claims text. ERROR findings must be zeroed; unmet quality thresholds mean the package is delivered labelled an incomplete draft, with the gaps listed.

## Output Contract

```text
Mode:
Source map coverage (P/E/F/C block counts):
Inventories completed:
Evidence ledger (features by support state):
Claims drafted / audited:
Validator results (errors, warnings, quality scores):
[TO CONFIRM] questions for the inventor:
Disclaimer acknowledged (drafting aid, not a patentability opinion):
```

## Check Scope

Follow `../ccf-common/references/handoff-modes.md` and `../ccf-common/references/task-modes.md`. Source material is private by default: do not send unpublished manuscripts or disclosures to external search or prior-art services without the user's explicit instruction. Novelty searching, when the user requests it, routes through `ccf-literature-searcher` and is reported as search results, never as a patentability conclusion.
