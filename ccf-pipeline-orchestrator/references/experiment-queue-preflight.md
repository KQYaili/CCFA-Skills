# Optional Experiment Queue: Read-Only Preflight

Owner: `ccf-pipeline-orchestrator` coordinates an explicitly authorized research campaign; `ccf-experiment-designer` decides the protocol and statistical unit; `ccf-research-engineer` owns the actual execution. This is **not an automatic scheduler**, daemon, cron task, SSH executor, experiment result or permission to use paid compute.

Use only when a campaign needs multiple dependent jobs, a grid of seeds/configurations, or GPU queue recovery. For a single run, use the existing research-engineer execution path. Avoid running two independent schedulers over one run directory.

## Manifest contract

The `scripts/experiment_queue_preflight.py` helper validates a **JSON** manifest without executing any commands, changing files, or accessing a GPU. Each queued job must declare its own output path, dependency list, GPU count, maximum attempts and estimated hours.

Example (placeholder commands; **do not execute without authorization**):

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

Save a manifest only when the user wants an executable campaign artifact, using the established task-owned directory. Then run:

```bash
python ccf-pipeline-orchestrator/scripts/experiment_queue_preflight.py --manifest path/to/queue.json
```

Output: job count, worst-case estimated GPU hours, dependency waves, and `PREFLIGHT_ONLY_REQUIRES_AUTHORIZED_SCHEDULER`. The helper deliberately **does not** run the command strings. Wave ordering is logical, not a promise about resource packing or completion.

## Safety and evidence rules

- **Budget gate:** estimate worst-case compute as the sum of `gpu_count × estimated_hours × max_attempts` per job, reject missing/invalid bounds and any campaign exceeding the owner's declared GPU-hour ceiling. Estimated runtimes are *assumptions*, not measured costs.
- **Dependency gate:** reject unknown/self dependencies, duplicate IDs, cycles and output destination collisions. Do not restart a downstream job before its upstream checkpoint is truly complete and validated.
- **Execution separation:** require independent, current authorization for SSH/remote machine selection, GPU resource acquisition, paid calls, code mutation, actual commands and output paths. A valid manifest is **not** authorization.
- **Result identity:** distinct seed, split, task IDs and real frozen protocol are prerequisites before inferring independent replicates. The preflight cannot establish them; use the existing experiment audit and claim-promotion gate after real execution.
- **Failure recovery:** retain each original failed/partial attempt; OOM retry must have a newly recorded attempt and cannot silently change the comparable experimental protocol. A resource fallback applied only to one winning arm is not a fair comparison.
- **Scheduler integration:** a separate authorized scheduler may use this plan as input, but must recheck state/remote availability, protect output destinations, manage bounded concurrency/retries and record actual outcomes; CCFA does not claim to ship those capabilities in this PR. Do not wrap a scheduler in a second cron/agent loop.
- **Human readability:** keep job IDs, commands, arguments, source paths, timestamps, budget figures, per-attempt observations and Diff legible. Do not add file hashes or cryptographic-content identifiers.

## Testing and limitations

Run `python ccf-pipeline-orchestrator/scripts/test_experiment_queue_preflight.py` for deterministic manifest validation cases. No GPU/SSH or real experiments are required for these tests. **Manual pilot** before deploying any actual scheduler: try a toy two-wave queue with mock commands; interrupt and restart; simulate OOM, missing upstream output, duplicate output, and stale job state; ensure no paid or irreversible action occurs without authorization. A passed unit test does not mean real scheduling was exercised.

## Provenance

Adapted at the workflow level from [ARIS experiment-queue](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) (MIT). This implementation does not vendor ARIS's SSH scheduler, reviewer backends, or existing environment digest system; it adds only a safe CCFA-native preflight and a clearly separated execution boundary.
