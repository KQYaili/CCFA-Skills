# Manual Acceptance Plan — Targeted Research Improvements

This plan is for the maintainer to run before merging. **No tests in this document were executed by the author of the PR.** Use only consenting example projects and avoid putting private manuscript details into public search strings.

## 1. Static and offline automated smoke

From repository root:

```bash
python ccf-pipeline-orchestrator/scripts/test_experiment_queue_preflight.py
python -m py_compile ccf-pipeline-orchestrator/scripts/experiment_queue_preflight.py ccf-pipeline-orchestrator/scripts/test_experiment_queue_preflight.py
python ccf-common/scripts/check_markdown_links.py --help
```

The Markdown check command above is **only help inspection**; invoke its documented actual audit command after confirming flags in its CLI. No network, GPU or external model should be required by the queue tests.

## 2. Novelty collision acceptance

**Case N1 — Known prior-art overlap:** Supply a research idea and one original paper with the same operation under equivalent assumptions. Ask `ccf-idea-reviewer` to check novelty. Expected: it reports a *demonstrated* collision only if it read the relevant original section, records exact location and recommends a narrow honest delta or pivot, without claiming stronger experimental evidence than supplied.

**Case N2 — Abstract-only lead:** Supply an abstract that *sounds* similar but whose algorithm is not in the material. Expected: `abstract-only/provisional`; no definitive scooped verdict, invented equation or low idea score from missing experiments.

**Case N3 — Privacy/no-web:** Ask for a conceptual check with external browsing prohibited. Expected: use only supplied evidence, `supplied-only` coverage, no private research sent to search.

## 3. Primary-source trace acceptance

**Case S1 — Fake support:** Create a draft sentence attributing a precise numerical conclusion to a real, accessible source that says something different. Expected: `CONTRADICTED` or `NARROWER` with page/table/section anchor; BibTeX existence alone is not `SUPPORTED`.

**Case S2 — Inaccessible source:** Source metadata available, method/results not accessible. Expected: `METADATA_ONLY` or `UNRESOLVED`, not verified content.

**Case S3 — Later correction:** Provide a correction or newer version changing a dependent conclusion. Expected: identify original and corrected versions; `OUTDATED` only if correction is actually inspected.

## 4. Publication figure acceptance

**Case F1 — Two methods, same tasks:** Provide paired task-level outcomes plus an aggregate. Expected: paired-difference plot is considered; aggregation unit, uncertainty definition, n, budgets and source paths are preserved. No invented results, and numeric chart may not be replaced by an illustration.

**Case F2 — Dense multi-panel export:** Export a real PDF at target column width. Expected: run existing geometry/text/alignment checks as applicable, visually inspect final PDF, report actual overlaps or too-small mathematical subscripts. A clean scan without visual inspection is not enough.

**Case F3 — Schematic:** Provide a pipeline image, ask for editable revision. Expected: route to existing SVG/Draw.io/Figma workflow, not quantitative Matplotlib or a raster-only image.

## 5. Experiment queue acceptance

The included unit test covers successful dependency waves, invalid budget, unknown/cyclic dependencies, duplicate outputs, invalid inputs and no execution. Then manually inspect one generated manifest:

1. Start with the example in [experiment-queue-preflight.md](../ccf-pipeline-orchestrator/references/experiment-queue-preflight.md) and save it in a temporary working folder.
2. Run `python ccf-pipeline-orchestrator/scripts/experiment_queue_preflight.py --manifest <path>`.
3. Confirm `status=PREFLIGHT_ONLY_REQUIRES_AUTHORIZED_SCHEDULER`, `commands_executed=false`, accurate worst-case GPU-hours, correct dependency waves, and zero created experiment output directories.
4. Alter the manifest to exceed `max_gpu_hours`; the command must fail without any process launch.
5. **Separate integration pilot only when explicitly authorized:** run toy harmless commands with an independently installed scheduler, test failed checkpoints, OOM-like failure, interruption/resume and output overwrite behavior. Those behaviors are **not implemented or proven by this PR**.

## 6. Regression boundaries

Verify normal single-paper reading, a local figure typography edit, a short idea review, and a manuscript text revision **do not** require new project state, experiment queue, paid model, new file or scorecard. Verify existing Benchmark templates and post-run experiment audit still route as before.

Do not merge solely because the Skill instructions read well. Review the actual user-facing output for N1/N2/S1/F1 against the source artifact, and confirm no new license-incompatible code, copied third-party plot assets or cryptographic checksum steps were added.
