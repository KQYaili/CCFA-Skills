# Optional Scientific Argument State (Per Paper)

Use only for **ongoing multi-session research manuscripts** where scientific questions, rival explanations, experiments, and writing can drift apart. Inspired by the project-context and paragraph-state ideas in [reyuyu/CCFA-GENT](https://github.com/reyuyu/CCFA-GENT), but independently specified for CCFA's existing evidence, artifact and manuscript workflows. It does **not** import CCFA-GENT's source code or UI.

**Default remains no state file.** For a short idea review, one paragraph, read-only literature lookup, or a task where the user declines new files, keep context in the existing artifacts and conversation. Avoid a second database.

## Ownership and location

- Use the paper's existing project record and `ccfa.yaml` claims, experiments, reviews and paths as authoritative. **Do not change the `ccfa.yaml` schema.**
- When explicitly useful and authorized, maintain *one optional* `scientific-argument.json` per manuscript, under its **existing project task directory** (for instance `ccfa-workfiles/ideas/<paper-id>/source/scientific-argument.json`). Do not create a new root folder merely to hold it.
- `ccf-pipeline-orchestrator` owns authorized cross-stage updates; `ccf-idea-optimizer` proposes questions/hypotheses; `ccf-experiment-designer` proposes experimental links; `ccf-integrity-auditor` verifies evidence; `ccf-paper-writer` uses it as framing; `ccf-paper-reviewer` challenges it. Except for an explicitly authorized owner, helpers **return proposed changes**, not independent writes.
- Preserve true evidence sources and records at their original paths. Evidence references are **pointers** (commit, table, record ID, exact passage), not pasted result tables or confirmation of inspection. The JSON file must never be taken as an empirical source merely because it states a claim.

## Minimal schema

```json
{
  "record_type": "ccfa-scientific-argument",
  "schema_version": 1,
  "paper_id": "paper-identifier",
  "scientific_question": "",
  "throughline": "",
  "hypotheses": [
    {
      "id": "H1",
      "statement": "",
      "rival": "",
      "prediction": "",
      "evidence_stage": "unassessed",
      "evidence_refs": []
    }
  ],
  "paragraphs": [
    {
      "id": "intro-claim-1",
      "section_id": "introduction",
      "status": "draft",
      "manuscript_sha256": null
    }
  ]
}
```

Empty hypothesis/paragraph arrays are valid. Unfilled fields are explicitly **unassessed**, not inferred. Hypothesis `evidence_stage` is one of `unassessed / exploratory / confirmatory / theoretical`: this records the *reported study category*, not proof that a result validates the hypothesis. The reference needs external verification; planned evidence is not observed evidence. Negative and mixed outcomes must remain usable.

For verified paragraphs, provide a current **full-file SHA-256** in `manuscript_sha256` plus `verification: {"scope": "<checked scope>", "receipt": "<actual audit/report anchor>"}`. This is a **versioned receipt for stated coverage**, not a global proof of correctness. Validate against `--manuscript` before reusing a previous verified status; an unchanged SHA supports version identity, not the sufficiency of the audit. Editing the paper makes prior receipts stale until rechecked. Freezing a paragraph means "do not casually rewrite", **not** "ignore factual errors".

## Paragraph lifecycle

To obtain the manuscript digest for a receipt, run the writer's [inspect command](../../ccf-paper-writer/references/writing-execution.md#prepare-only-the-material-needed) and copy its `sha256` field. Its UTC modification time and byte count help you recognize the file during a handoff.

- `todo`: not written; no claim of missing evidence unless checked.
- `draft`: working prose; ordinary authorized revisions are permitted.
- `review`: under review; reviewer does not gain edit rights.
- `frozen`: preserve style and content by default; scientific or numerical faults **must still be reported**, with the relevant source and repair scope.
- `verified`: checked at the declared scope against the declared exact manuscript version; still subject to superseding evidence, broader review and current venue rules.

Status is a workflow hint; it does not override the user's current instructions, human editorial choice, the manuscript itself, or scientific integrity.

## Lightweight helper (no network / no manuscript editing)

The script `ccf-common/scripts/scientific_argument.py` supports:

```bash
python ccf-common/scripts/scientific_argument.py init --file ccfa-workfiles/ideas/my-paper/source/scientific-argument.json --paper-id my-paper
python ccf-common/scripts/scientific_argument.py validate --file ccfa-workfiles/ideas/my-paper/source/scientific-argument.json --manuscript manuscript/main.tex
python ccf-common/scripts/scientific_argument.py brief --file ccfa-workfiles/ideas/my-paper/source/scientific-argument.json
```

`init` refuses to overwrite; the parent directory must already exist. `validate` checks **structure and version-staleness**, not whether scientific claims are true. `brief` prints a small `{"message": ..., "throughline": ...}` object compatible with the writer's existing `--brief` input; it refuses to export a blank question/throughline. Save the output as the existing task's brief only when needed, under an authorized path. The original hypotheses and evidence refs remain in the argument file, not duplicated into a new "facts" database.

## Handoff discipline

For substantial authorized work, compare the scientific question and selected hypothesis to the **actual manuscript and experiment records**, explicitly noting contradictions and uncertainty. If the hypothesis and new evidence conflict, correct or narrow the claim; **do not retrofit the observations to the original narrative**. Preserve each paper's independent question and evidence boundary even when papers share an experimental repository. A source/commit/version mismatch blocks only the dependent claim, not unrelated drafting.

## Attribution and limits

Conceptual inspiration: CCFA-GENT's project-level problem memory, paragraph status and confirmation-first interface. The CCFA reference and helper are original implementations; CCFA-GENT's README currently does not declare a license. This extension is a documented optional workflow, **not** a standalone web application, automatic external-reference importer, or continuous background synchronizer.
