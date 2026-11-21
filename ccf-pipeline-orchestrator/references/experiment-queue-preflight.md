# Experiment Queue Preflight

When reviewing a proposed GPU campaign, the orchestrator can check job dependencies, estimated GPU hours and output destinations from a local JSON file. The experiment designer owns the protocol and unit of replication. The research engineer owns execution under the campaign's existing authorization.

## Manifest contract

Each job declares a unique ID, command string, working directory, output path, GPU count and estimated hours per attempt. Omitted `depends_on` defaults to an empty list and omitted `max_attempts` defaults to one. The helper reads UTF-8 JSON with unique field names. Hour estimates and ceilings must be finite positive numbers in the range of a nonzero Python float.

The helper uses the path conventions of the host running the check. For a cross-platform campaign, verify destinations on the execution platform. Relative `cwd` starts at the manifest directory. Relative `output` starts at that job's `cwd`. The check compares normalized destination paths, including `.`, `..` and native separators, with Windows case folding and POSIX case-sensitive spelling. Use fully qualified paths for drive-qualified Windows destinations. Link aliases, case-insensitive POSIX volumes, nested directory ownership and existing files require inspection on the execution host.

```json
{
  "schema_version": 1,
  "project": "paper-p1-demo",
  "limits": {
    "max_jobs": 3,
    "max_parallel": 2,
    "max_attempts": 2,
    "max_gpu_hours": 12
  },
  "jobs": [
    {
      "id": "baseline-seed-1",
      "command": "python run_baseline.py --seed 1",
      "cwd": "paper-project",
      "output": "runs/baseline-seed-1/results.json",
      "depends_on": [],
      "gpu_count": 1,
      "estimated_hours": 2,
      "max_attempts": 2
    },
    {
      "id": "abl-seed-1",
      "command": "python run_ablation.py --seed 1",
      "cwd": "paper-project",
      "output": "runs/abl-seed-1/results.json",
      "depends_on": ["baseline-seed-1"],
      "gpu_count": 1,
      "estimated_hours": 2,
      "max_attempts": 2
    }
  ]
}
```

Check a manifest from the repository root.

```bash
python ccf-pipeline-orchestrator/scripts/experiment_queue_preflight.py --manifest path/to/queue.json
```

The example returns two dependency waves and eight estimated GPU-hours if both jobs use both attempts. It reads the manifest without launching its commands or creating job directories. A valid manifest produces a JSON report on stdout with exit code 0. Invalid manifests produce a JSON diagnostic on stderr with exit code 2.

## Interpreting the report

- `worst_case_gpu_hours` sums `gpu_count × estimated_hours × max_attempts` across jobs. The budget comparison uses the declared decimal values before display rounding. Actual costs depend on measured runtimes.
- `dependency_waves` groups jobs whose declared prerequisites appear in earlier waves. One wave can exceed `max_parallel_jobs`. The executor must enforce the parallel-job ceiling and check hardware availability and upstream completion.
- Job IDs and distinct outputs identify planned work. The experiment designer evaluates independence, failure handling and protocol comparability using the resulting run records.

## Validation

Run `python ccf-pipeline-orchestrator/scripts/test_experiment_queue_preflight.py` for offline API and CLI tests.

## Provenance

The bounded-queue workflow was inspired by [ARIS](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep).
