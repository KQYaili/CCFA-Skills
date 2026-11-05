---
name: ccf-proposal-writer
description: "Draft, revise, or audit research proposals, grant applications, and opening reports as an evidence-first state machine with per-section contracts and layered QA. Use for 基金申请书, NSFC申请, 开题报告, 研究方案, proposal drafting, and proposal review. Manuscripts for venue submission belong to ccf-paper-writer; concept judgment belongs to ccf-idea-reviewer."
metadata:
  ccf_skill_controls:
    handoff_question_mode: partial
    respect_session_denylists: true
    protect_idea_scope_in_writing: true
    private_material_safety: moderate
    shared_controls: ../ccf-common/references/
---

# CCF Proposal Writer

## Family File Contract

Before file work, reuse canonical paths and one task/artifact working directory; default to project-root `ccfa-workfiles/<purpose>/<artifact-id>/`. Update in place, preserve inputs, and use UTF-8 with Chinese-text checks. Apply [artifact-contracts.md](../ccf-common/references/artifact-contracts.md) for naming, ownership, and task-created cleanup; handoffs inherit these paths.

## Collaboration Contract

Before specialist execution, read and apply [ccf-humanization](../ccf-humanization/SKILL.md) first, then [ccf-common](../ccf-common/SKILL.md). At every handoff, reuse their applicable active rules or refresh missing/changed ones. Both preflights are required even without prose; detailed editing, experiment, and maintenance modes run only when relevant.

Integrate necessary specialist contributions under one owner; reuse valid prerequisites and verify affected results. Follow the [cooperation routes](../ccf-common/references/routing.md) without duplicate reports.

## Core Rule

A proposal is a promise calibrated to evidence. Never draft prose before the evidence base exists, never let a section claim more than its contract allows, and never upgrade a hedged statement ("may indicate") into a strong one ("proves") without evidence that supports the upgrade. When the evidence cannot carry the original promise, lower the commitment instead of explaining the gap away. Do not invent funding history, personnel, preliminary results, or institutional facts; mark missing facts as questions, not as plausible filler.

## Modes

- `compose`: from a topic, direction, or rough idea to a full proposal through the foundation files.
- `revise`: diagnose and revise an existing paragraph, section, or full proposal.
- `hybrid`: revise an existing draft while extending, completing, or restructuring it.
- `qa`: run the four-gate QA pipeline over supplied text without drafting new content.

## Workflow

1. Establish the foundation files before drafting (see [proposal-state-machine.md](references/proposal-state-machine.md)): `00_scope.md` (task boundary), `01_research_canon.md` (hard facts and constraints), `02_evidence_table.md` (claim-to-evidence map), `03_argument_map.md` (argument architecture), `04_section_contracts.md` (per-section purpose, inputs, allowed and forbidden claims), `05_style_guide.md` (terminology and banned expressions), plus `state.json` (mode, round, scores, technical debts).
2. Check scope before completeness: for phased writing, lock the phase boundary first and refuse scope creep outside it.
3. Draft or revise section by section against the section contracts; a claim with no evidence-table entry does not enter the text.
4. Run QA in gate order (see [proposal-qa-gates.md](references/proposal-qa-gates.md)): content experts matched to the failure mode first, language checks second, mechanical validation third, scored threshold last. Content before language — never polish a sentence an expert gate is about to reject.
5. Apply the scenario threshold (paper 7.0, proposal 7.0, internal 5.0, quick = P0 findings only). Below threshold, roll back only the low-scoring dimensions, at most 3 rounds.
6. When a core promise outruns the evidence, switch to commitment-lowering mode and apply the stop rules (see [commitment-lowering-and-stopping.md](references/commitment-lowering-and-stopping.md)): plateau, unresolved expert conflict, and missing evidence for a key claim are stop reasons, not polishing reasons.

## Output Contract

```text
Mode:
Foundation state (files present / missing):
Sections drafted or revised:
QA gates run and scenario threshold:
Scores by dimension (if scored):
Commitment changes (lowered claims and why):
Remaining risks:
Next step:
```

## Check Scope

Follow `../ccf-common/references/handoff-modes.md` and `../ccf-common/references/task-modes.md`. Literature grounding for the canon and evidence table routes to `ccf-literature-searcher`; concept worthiness routes to `ccf-idea-reviewer`; turning an accepted proposal into a venue manuscript routes to `ccf-paper-writer`. Authorship, affiliation, and funding statements use only facts the user supplies; the default independent-researcher acknowledgement wording lives with the user's own conventions, not in generated filler.
