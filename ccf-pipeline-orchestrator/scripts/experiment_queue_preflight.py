#!/usr/bin/env python3
"""Read-only preflight of a proposed GPU experiment queue.

Inputs: JSON with project, jobs, resource ceiling. No process launching,
SSH, installs, network, job killing, run-history updates or file mutation.
"""
import argparse
import json
import sys
from pathlib import Path


class QueueSpecError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise QueueSpecError(message)


def positive_int(value, name, zero=False):
    require(type(value) is int and value >= (0 if zero else 1),
            f"{name} must be an integer >= {0 if zero else 1}")
    return value


def nonempty(value, name):
    require(isinstance(value, str) and bool(value.strip()),
            f"{name} must be a nonempty string")
    return value


def audit(spec):
    """Return an inspectable plan; never run any declared command."""
    require(isinstance(spec, dict), "root must be an object")
    project = nonempty(spec.get("project"), "project")
    require(spec.get("schema_version") == 1, "schema_version must be 1")
    budget = spec.get("limits")
    require(isinstance(budget, dict), "limits must be an object")
    max_jobs = positive_int(budget.get("max_jobs"), "limits.max_jobs")
    max_parallel = positive_int(budget.get("max_parallel"), "limits.max_parallel")
    max_attempts = positive_int(budget.get("max_attempts"), "limits.max_attempts")
    max_gpu_hours = budget.get("max_gpu_hours")
    require(type(max_gpu_hours) in (int, float) and 0 < max_gpu_hours < 1e8,
            "limits.max_gpu_hours must be finite and positive")
    require(isinstance(spec.get("jobs"), list) and spec["jobs"], "jobs must be a nonempty list")
    require(len(spec["jobs"]) <= max_jobs, "job count exceeds max_jobs")
    require(max_parallel <= max_jobs, "max_parallel cannot exceed max_jobs")

    jobs = {}
    paths = set()
    expected = 0.0
    for pos, raw in enumerate(spec["jobs"]):
        require(isinstance(raw, dict), f"jobs[{pos}] must be an object")
        name = nonempty(raw.get("id"), f"jobs[{pos}].id")
        require(name not in jobs, "duplicate job ID: " + name)
        cmd = nonempty(raw.get("command"), f"jobs[{pos}].command")
        # Commands are data only and must never be evaluated by the preflight.
        working_dir = nonempty(raw.get("cwd"), f"jobs[{pos}].cwd")
        output = nonempty(raw.get("output"), f"jobs[{pos}].output")
        require(output not in paths, "duplicate output destination: " + output)
        paths.add(output)
        depends = raw.get("depends_on", [])
        require(isinstance(depends, list) and all(isinstance(x, str) and x for x in depends),
                "depends_on must be a list of IDs for " + name)
        require(len(depends) == len(set(depends)), "duplicate dependency for " + name)
        gpu = positive_int(raw.get("gpu_count"), f"{name}.gpu_count")
        hours = raw.get("estimated_hours")
        require(type(hours) in (int, float) and 0 < hours < 1e8,
                f"{name}.estimated_hours must be finite and positive")
        attempts = positive_int(raw.get("max_attempts", 1), f"{name}.max_attempts")
        require(attempts <= max_attempts, f"{name}.max_attempts exceeds global ceiling")
        expected += gpu * hours * attempts
        jobs[name] = {"id": name, "command": cmd, "cwd": working_dir, "output": output,
                      "depends_on": depends, "gpu_count": gpu,
                      "estimated_hours": hours, "max_attempts": attempts}

    require(expected <= max_gpu_hours,
            f"worst-case GPU hours {expected:.3f} exceed limit {max_gpu_hours}")
    for name, job in jobs.items():
        for dep in job["depends_on"]:
            require(dep in jobs, f"unknown dependency: {name} -> {dep}")
            require(dep != name, f"self-dependency: {name}")

    pending = set(jobs)
    waves = []
    done = set()
    while pending:
        ready = sorted(name for name in pending if set(jobs[name]["depends_on"]) <= done)
        require(ready, "dependency cycle detected")
        # This is a conservative plan of dependency waves, not real GPU packing.
        # Do not claim a wave has completed before the actual scheduler confirms it.
        waves.append(ready)
        done.update(ready)
        pending.difference_update(ready)

    return {
        "valid": True, "project": project, "job_count": len(jobs),
        "max_parallel_jobs": max_parallel, "worst_case_gpu_hours": round(expected, 4),
        "resource_limit_gpu_hours": max_gpu_hours, "dependency_waves": waves,
        "commands_executed": False,
        "status": "PREFLIGHT_ONLY_REQUIRES_AUTHORIZED_SCHEDULER",
        "limitations": [
            "Does not inspect remote GPU availability, model/data licenses, live checkpoints or command effects",
            "Estimated hours are inputs, not measured compute; caller must validate budget assumptions",
            "Wave order is a dependency order, not a fully scheduled GPU timeline",
            "Job execution and retries require explicit authorization and a separate installed scheduler"
        ]
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, help="Local UTF-8 JSON queue manifest")
    args = parser.parse_args(argv)
    try:
        payload = json.loads(Path(args.manifest).read_text(encoding="utf-8"))
        result = audit(payload)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
