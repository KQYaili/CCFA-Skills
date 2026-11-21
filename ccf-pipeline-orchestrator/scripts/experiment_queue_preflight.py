#!/usr/bin/env python3
"""Read-only preflight of a proposed GPU experiment queue.

Inputs: JSON with project, jobs, resource ceiling. No process launching,
SSH, installs, network, job killing, run-history updates or file mutation.
"""
import argparse
from decimal import Decimal, InvalidOperation
from fractions import Fraction
from graphlib import CycleError, TopologicalSorter
import json
import os
import sys
from pathlib import Path


class QueueSpecError(ValueError):
    pass


def require(ok, message):
    if not ok:
        raise QueueSpecError(message)


def positive_int(value, name):
    require(type(value) is int and value >= 1, f"{name} must be a positive integer")
    return value


def nonempty(value, name):
    require(isinstance(value, str) and bool(value.strip()),
            f"{name} must be a nonempty string")
    return value


def hours_value(value, name):
    # Accept ordinary Python numbers in audit() and the exact decimal tokens from JSON.
    require(type(value) in (int, float, Decimal)
            and (not isinstance(value, Decimal) or value.is_finite())
            and 0 < value <= sys.float_info.max and float(value) > 0,
            f"{name} must be a finite positive number within the supported numeric range")
    return Fraction(str(value))


def report_number(value):
    return value.numerator if value.denominator == 1 else float(value)


def audit(spec, *, base_dir=None):
    """Return an inspectable plan; never run any declared command."""
    require(isinstance(spec, dict), "root must be an object")
    project = nonempty(spec.get("project"), "project")
    require(type(spec.get("schema_version")) is int and spec["schema_version"] == 1, "schema_version must be 1")
    budget = spec.get("limits")
    require(isinstance(budget, dict), "limits must be an object")
    max_jobs = positive_int(budget.get("max_jobs"), "limits.max_jobs")
    max_parallel = positive_int(budget.get("max_parallel"), "limits.max_parallel")
    max_attempts = positive_int(budget.get("max_attempts"), "limits.max_attempts")
    max_gpu_hours = hours_value(budget.get("max_gpu_hours"), "limits.max_gpu_hours")
    require(isinstance(spec.get("jobs"), list) and spec["jobs"], "jobs must be a nonempty list")
    require(len(spec["jobs"]) <= max_jobs, "job count exceeds max_jobs")
    require(max_parallel <= max_jobs, "max_parallel cannot exceed max_jobs")

    dependencies = {}
    paths = set()
    expected = Fraction(0)
    base_dir = os.path.abspath(base_dir or ".")
    for pos, raw in enumerate(spec["jobs"]):
        require(isinstance(raw, dict), f"jobs[{pos}] must be an object")
        name = nonempty(raw.get("id"), f"jobs[{pos}].id")
        require(name not in dependencies, "duplicate job ID: " + name)
        nonempty(raw.get("command"), f"jobs[{pos}].command")
        # Commands are data only and must never be evaluated by the preflight.
        working_dir = nonempty(raw.get("cwd"), f"jobs[{pos}].cwd")
        output = nonempty(raw.get("output"), f"jobs[{pos}].output")
        for path in (working_dir, output):
            require("\0" not in path, f"{name}: paths cannot contain a null character")
            require(not os.path.splitdrive(path)[0] or os.path.isabs(path),
                    f"{name}: use a fully qualified or relative path rather than a drive-relative path")
        destination = os.path.normcase(os.path.normpath(os.path.join(base_dir, working_dir, output)))
        require(destination not in paths, "duplicate output destination: " + output)
        paths.add(destination)
        depends = raw.get("depends_on", [])
        require(isinstance(depends, list) and all(isinstance(x, str) and x for x in depends),
                "depends_on must be a list of IDs for " + name)
        require(len(depends) == len(set(depends)), "duplicate dependency for " + name)
        gpu = positive_int(raw.get("gpu_count"), f"{name}.gpu_count")
        hours = hours_value(raw.get("estimated_hours"), f"{name}.estimated_hours")
        attempts = positive_int(raw.get("max_attempts", 1), f"{name}.max_attempts")
        require(attempts <= max_attempts, f"{name}.max_attempts exceeds global ceiling")
        expected += gpu * hours * attempts
        dependencies[name] = depends

    require(expected <= max_gpu_hours,
            f"estimated GPU hours across all attempts exceed limit {budget['max_gpu_hours']}")
    for name, parents in dependencies.items():
        for dep in parents:
            require(dep in dependencies, f"unknown dependency: {name} -> {dep}")
            require(dep != name, f"self-dependency: {name}")

    graph = TopologicalSorter(dependencies)
    try:
        graph.prepare()
    except CycleError as exc:
        raise QueueSpecError("dependency cycle detected") from exc
    waves = []
    while graph.is_active():
        ready = sorted(graph.get_ready())
        waves.append(ready)
        graph.done(*ready)

    return {
        "valid": True, "project": project, "job_count": len(dependencies),
        "max_parallel_jobs": max_parallel, "worst_case_gpu_hours": report_number(expected),
        "resource_limit_gpu_hours": report_number(max_gpu_hours), "dependency_waves": waves,
        "commands_executed": False,
        "status": "preflight_only",
        "limitations": [
            "Does not inspect remote GPU availability, model/data licenses, live checkpoints or command effects",
            "Estimated hours are inputs, not measured compute; caller must validate budget assumptions",
            "Wave order is a dependency order, not a fully scheduled GPU timeline",
            "Execution and retries are handled by the workflow that runs the jobs"
        ]
    }


def unique_fields(pairs):
    record = {}
    for name, value in pairs:
        require(name not in record, f"duplicate JSON field: {name}")
        record[name] = value
    return record


def reject_constant(token):
    raise QueueSpecError(f"invalid JSON number: {token}")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path, help="Local UTF-8 JSON queue manifest")
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.manifest.read_text(encoding="utf-8-sig"), parse_float=Decimal,
                             object_pairs_hook=unique_fields, parse_constant=reject_constant)
        result = audit(payload, base_dir=args.manifest.parent)
    except (OSError, ValueError, InvalidOperation, RecursionError) as exc:
        print(json.dumps({"valid": False, "error": str(exc)}), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
