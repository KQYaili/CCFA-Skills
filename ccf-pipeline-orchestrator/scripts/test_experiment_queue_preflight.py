#!/usr/bin/env python3
"""Offline, deterministic tests for the optional read-only experiment queue preflight."""
import copy
import unittest

from experiment_queue_preflight import QueueSpecError, audit


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


if __name__ == "__main__":
    unittest.main()
