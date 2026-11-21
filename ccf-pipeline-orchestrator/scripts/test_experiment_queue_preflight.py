#!/usr/bin/env python3
"""Offline, deterministic tests for the optional read-only experiment queue preflight."""
import copy
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from experiment_queue_preflight import QueueSpecError, audit

CLI = Path(__file__).with_name("experiment_queue_preflight.py").resolve()


def sample():
    return {
        "schema_version": 1,
        "project": "toy-queue",
        "limits": {
            "max_jobs": 3,
            "max_parallel": 2,
            "max_attempts": 2,
            "max_gpu_hours": 9
        },
        "jobs": [
            {"id": "start", "command": "echo start", "cwd": "tmp", "output": "out/start.json",
             "depends_on": [], "gpu_count": 1, "estimated_hours": 2, "max_attempts": 2},
            {"id": "follow", "command": "echo follow", "cwd": "tmp", "output": "out/follow.json",
             "depends_on": ["start"], "gpu_count": 1, "estimated_hours": 2, "max_attempts": 2}
        ]
    }


class ExperimentQueuePreflightTests(unittest.TestCase):
    def test_two_waves_budget_and_no_execution(self):
        manifest = sample()
        original = copy.deepcopy(manifest)
        result = audit(manifest)
        self.assertTrue(result["valid"])
        self.assertEqual(result["status"], "preflight_only")
        self.assertEqual(result["dependency_waves"], [["start"], ["follow"]])
        self.assertEqual(result["worst_case_gpu_hours"], 8)
        self.assertFalse(result["commands_executed"])
        self.assertEqual(manifest, original)

    def test_duplicate_output_is_blocked(self):
        s = sample()
        s["jobs"][1]["output"] = s["jobs"][0]["output"]
        with self.assertRaisesRegex(QueueSpecError, "duplicate output"):
            audit(s)

    def test_missing_dependency_is_blocked(self):
        s = sample()
        s["jobs"][1]["depends_on"] = ["not-a-job"]
        with self.assertRaisesRegex(QueueSpecError, "unknown dependency"):
            audit(s)

    def test_destinations_use_job_directory_and_manifest_base(self):
        with tempfile.TemporaryDirectory() as folder:
            s = sample()
            first, second = s["jobs"]
            first.update(cwd="project", output="out/scores.json")
            second.update(cwd="another", output="out/scores.json")
            self.assertTrue(audit(s, base_dir=folder)["valid"])
            for cwd, output in [("another", "../project/out/./scores.json"),
                                (".", str(Path(folder) / "project/out/scores.json"))]:
                with self.subTest(cwd=cwd, output=output):
                    second.update(cwd=cwd, output=output)
                    with self.assertRaisesRegex(QueueSpecError, "duplicate output"):
                        audit(s, base_dir=folder)
            self.assertEqual(list(Path(folder).iterdir()), [])

    def test_output_path_case_uses_host_path_rules(self):
        s = sample()
        s["jobs"][0]["output"] = "results.json"
        s["jobs"][1]["output"] = "Results.json"
        if os.path.normcase("A") == os.path.normcase("a"):
            with self.assertRaisesRegex(QueueSpecError, "duplicate output"):
                audit(s)
        else:
            self.assertTrue(audit(s)["valid"])

    def test_null_character_is_rejected_in_both_path_fields(self):
        for field in ("cwd", "output"):
            s = sample()
            s["jobs"][0][field] = "bad\0path"
            with self.subTest(field=field), self.assertRaisesRegex(QueueSpecError, "null character"):
                audit(s)

    def test_waves_describe_dependencies_independently_of_parallel_ceiling(self):
        s = sample()
        s["jobs"][1]["depends_on"] = []
        s["limits"]["max_parallel"] = 1
        result = audit(s)
        self.assertEqual(result["max_parallel_jobs"], 1)
        self.assertEqual(result["dependency_waves"], [["follow", "start"]])

    def test_cycle_is_blocked(self):
        s = sample()
        s["jobs"][0]["depends_on"] = ["follow"]
        with self.assertRaisesRegex(QueueSpecError, "cycle"):
            audit(s)

    def test_budget_ceiling_is_blocked(self):
        s = sample()
        s["limits"]["max_gpu_hours"] = 7
        with self.assertRaisesRegex(QueueSpecError, "exceed limit"):
            audit(s)

    def test_attempts_ceiling_is_blocked(self):
        s = sample()
        s["jobs"][0]["max_attempts"] = 3
        with self.assertRaisesRegex(QueueSpecError, "exceeds global"):
            audit(s)

    def test_fractional_hours_at_and_above_ceiling(self):
        s = sample()
        for job, hours in zip(s["jobs"], [.1, .2]):
            job.update(estimated_hours=hours, max_attempts=1)
        s["limits"]["max_gpu_hours"] = .3
        self.assertEqual(audit(s)["worst_case_gpu_hours"], .3)
        s["limits"]["max_gpu_hours"] = .29999999999999993
        with self.assertRaisesRegex(QueueSpecError, "exceed limit"):
            audit(s)
        for job in s["jobs"]:
            job["estimated_hours"] = .000001
        self.assertEqual(audit(s)["worst_case_gpu_hours"], .000002)

    def test_large_gpu_count_is_a_budget_error(self):
        s = sample()
        s["jobs"][0].update(gpu_count=10**400, estimated_hours=.1)
        with self.assertRaisesRegex(QueueSpecError, "exceed limit"):
            audit(s)

    def test_boolean_not_accepted_as_integer(self):
        s = sample()
        s["limits"]["max_jobs"] = True
        with self.assertRaisesRegex(QueueSpecError, "integer"):
            audit(s)

    def test_bad_runtime_and_empty_job_command_are_blocked(self):
        s = sample()
        s["jobs"][0]["estimated_hours"] = 0
        with self.assertRaisesRegex(QueueSpecError, "positive"):
            audit(s)
        s = sample()
        s["jobs"][0]["command"] = " "
        with self.assertRaisesRegex(QueueSpecError, "nonempty"):
            audit(s)


class QueueCLITests(unittest.TestCase):
    def run_cli(self, manifest):
        return subprocess.run([sys.executable, "-B", str(CLI), "--manifest", str(manifest)],
                              cwd=manifest.parent.parent, capture_output=True, text=True,
                              encoding="utf-8", timeout=10)

    def test_reads_manifest_relative_paths_without_creating_job_outputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            folder = root / "manifests"
            folder.mkdir()
            working_dir = folder / "tmp"
            working_dir.mkdir()
            manifest = folder / "queue.json"
            s = sample()
            for job in s["jobs"]:
                job["command"] = "echo ran > marker.txt"
            original = json.dumps(s).encode("utf-8-sig")
            manifest.write_bytes(original)
            result = self.run_cli(manifest)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(json.loads(result.stdout)["commands_executed"])
            self.assertEqual(set(root.rglob("*")), {folder, working_dir, manifest})
            self.assertEqual(manifest.read_bytes(), original)
            s["jobs"][1]["output"] = str(folder / "tmp/out/start.json")
            manifest.write_text(json.dumps(s), encoding="utf-8")
            result = self.run_cli(manifest)
            self.assertEqual(result.returncode, 2)
            self.assertIn("duplicate output", json.loads(result.stderr)["error"])

    def test_cli_checks_original_decimal_digits_and_rejects_ambiguous_input(self):
        s = sample()
        s["jobs"] = [dict(s["jobs"][0], estimated_hours="HOURS", max_attempts=1)]
        s["limits"]["max_gpu_hours"] = .3
        text = json.dumps(s)
        bad = {
            "precision": (text.replace('"HOURS"', "0.3000000000000000000000000001"), "exceed limit"),
            "duplicate key": ('{"limits": {}, "limits": {}}', "duplicate JSON field"),
            "infinite": (text.replace('"HOURS"', "Infinity"), "invalid JSON number"),
            "wrong shape": ("[]", "root must be an object"),
            "invalid JSON": ("{", "Expecting"),
        }
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / "queue.json"
            result = self.run_cli(manifest)
            self.assertEqual(result.returncode, 2)
            self.assertFalse(json.loads(result.stderr)["valid"])
            for case, (source, message) in bad.items():
                with self.subTest(case=case):
                    manifest.write_text(source, encoding="utf-8")
                    result = self.run_cli(manifest)
                    self.assertEqual(result.returncode, 2)
                    self.assertEqual(result.stdout, "")
                    self.assertIn(message, json.loads(result.stderr)["error"])


if __name__ == "__main__":
    unittest.main()
