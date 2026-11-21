"""Offline regression tests for optional argument state and review-before-apply patches."""
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]


def module_at(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


argument = module_at("ccfa_scientific_argument", ROOT / "ccf-common/scripts/scientific_argument.py")
patching = module_at("ccfa_manuscript_patch", ROOT / "ccf-paper-writer/scripts/manuscript_patch.py")


class ArgumentStateTests(unittest.TestCase):
    def test_blank_state_and_nonoverwriting_init(self):
        with tempfile.TemporaryDirectory() as folder:
            state = Path(folder) / "argument.json"
            result = argument.cli(["init", "--file", str(state), "--paper-id", "P1"])
            self.assertEqual(result["created"], str(state))
            self.assertFalse(argument.validate(json.loads(state.read_text()))["ready_for_brief"])
            with self.assertRaises(FileExistsError):
                argument.cli(["init", "--file", str(state), "--paper-id", "P1"])

    def test_brief_and_stale_verification(self):
        with tempfile.TemporaryDirectory() as folder:
            paper = Path(folder) / "paper.md"
            paper.write_text("# Introduction\nA claim.\n", encoding="utf-8")
            state = argument.example("P2")
            state["scientific_question"] = "What causes error repetition?"
            state["throughline"] = "Hold submitted answers fixed; change checker inputs."
            self.assertEqual(argument.validate(state)["ready_for_brief"], True)
            statefile = Path(folder) / "argument.json"
            statefile.write_text(json.dumps(state), encoding="utf-8")
            brief = argument.cli(["brief", "--file", str(statefile)])
            self.assertEqual(brief["message"], state["scientific_question"])
            state["paragraphs"] = [{"id": "intro-a", "section_id": "introduction",
                                    "status": "verified", "manuscript_sha256": "a" * 64,
                                    "verification": {"scope": "paragraph", "receipt": "review#3"}}]
            with self.assertRaisesRegex(ValueError, "stale"):
                argument.validate(state, manuscript=paper)
            state["paragraphs"][0]["status"] = "frozen"
            self.assertTrue(argument.validate(state, manuscript=paper)["valid"])


class PatchPreviewTests(unittest.TestCase):
    def test_preview_has_diff_but_no_write(self):
        with tempfile.TemporaryDirectory() as folder:
            paper = Path(folder).resolve() / "paper.md"
            original = b"# Method\r\nOld claim."
            paper.write_bytes(original)
            inventory = patching.inspect_manuscript(paper)
            packet = {"schema_version": 1, "operation": "write",
                      "manuscript": {"path": str(paper), "sha256": inventory["sha256"]},
                      "targets": ["method"], "dependencies": []}
            proposed = {"base_sha256": inventory["sha256"],
                        "edits": [{"section_id": "method", "before": "Old claim.", "after": "Revised claim."}]}
            preview = patching.apply_patch(packet, proposed, dry_run=True)
            self.assertTrue(preview["changed"])
            self.assertIn("-Old claim.\n\\ No newline at end of file\n"
                          "+Revised claim.\n\\ No newline at end of file\n", preview["unified_diff"])
            self.assertEqual(paper.read_bytes(), original)
            self.assertEqual(preview["before_revision"], inventory["revision"])
            applied = patching.apply_patch(packet, proposed)
            self.assertTrue(applied["changed"])
            self.assertEqual(paper.read_bytes(), b"# Method\r\nRevised claim.")
            self.assertEqual(preview["after_bytes"], paper.stat().st_size)
            self.assertEqual(preview["after_sha256"], applied["after_sha256"])
            with self.assertRaisesRegex(ValueError, "changed"):
                patching.apply_patch(packet, proposed, dry_run=True)

    def test_same_size_and_timestamp_do_not_authorize_a_stale_patch(self):
        with tempfile.TemporaryDirectory() as folder:
            paper = Path(folder).resolve() / "paper.md"
            paper.write_bytes(b"# Method\nRev A.\n")
            timestamp = (1609459200, 1609459200)
            os.utime(paper, timestamp)
            first = patching.inspect_manuscript(paper)
            packet = {"schema_version": 1, "manuscript": {"path": str(paper), "sha256": first["sha256"]},
                      "targets": ["method"], "dependencies": []}
            patch = {"base_sha256": first["sha256"],
                     "edits": [{"section_id": "method", "before": "Rev", "after": "Version"}]}
            paper.write_bytes(b"# Method\nRev B.\n")
            os.utime(paper, timestamp)
            second = patching.inspect_manuscript(paper)
            self.assertEqual(first["revision"], second["revision"])
            for dry_run in (True, False):
                with self.subTest(dry_run=dry_run), self.assertRaisesRegex(ValueError, "manuscript changed"):
                    patching.apply_patch(packet, patch, dry_run=dry_run)
            self.assertEqual(paper.read_bytes(), b"# Method\nRev B.\n")

    def test_read_only_review_packet_rejects_preview(self):
        with tempfile.TemporaryDirectory() as folder:
            paper = Path(folder).resolve() / "paper.md"
            paper.write_text("# Methods\nNo edit.\n", encoding="utf-8")
            inventory = patching.inspect_manuscript(paper)
            packet = {"schema_version": 1, "operation": "review",
                      "manuscript": {"path": str(paper), "sha256": inventory["sha256"]},
                      "targets": ["methods"], "dependencies": []}
            with self.assertRaisesRegex(ValueError, "read-only"):
                patching.apply_patch(packet, {"base_sha256": inventory["sha256"], "edits": []},
                                     dry_run=True)


if __name__ == "__main__":
    unittest.main()
