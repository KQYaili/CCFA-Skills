"""Offline regression tests for optional argument state and review-before-apply patches."""
from __future__ import annotations

import importlib.util
import json
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
                                    "status": "verified", "manuscript_version": "2001-01-01T00:00:00.000000+00:00 | 1 bytes",
                                    "verification": {"scope": "paragraph", "receipt": "review#3"}}]
            with self.assertRaisesRegex(ValueError, "stale"):
                argument.validate(state, manuscript=paper)
            state["paragraphs"][0]["status"] = "frozen"
            self.assertTrue(argument.validate(state, manuscript=paper)["valid"])


class PatchPreviewTests(unittest.TestCase):
    def test_preview_has_diff_but_no_write(self):
        with tempfile.TemporaryDirectory() as folder:
            paper = Path(folder) / "paper.md"
            paper.write_text("# Method\nOld claim.\n", encoding="utf-8")
            inventory = patching.inspect_manuscript(paper)
            packet = {"schema_version": 1, "operation": "write",
                      "manuscript": {"path": str(paper), "version": inventory["version"]},
                      "targets": ["method"], "dependencies": []}
            proposed = {"base_version": inventory["version"],
                        "edits": [{"section_id": "method", "before": "Old claim.", "after": "New claim."}]}
            preview = patching.apply_patch(packet, proposed, dry_run=True)
            self.assertTrue(preview["changed"])
            self.assertIn("-Old claim.", preview["unified_diff"])
            self.assertIn("+New claim.", preview["unified_diff"])
            self.assertIn("Old claim.", paper.read_text())
            applied = patching.apply_patch(packet, proposed)
            self.assertTrue(applied["changed"])
            self.assertIn("New claim.", paper.read_text())
            with self.assertRaisesRegex(ValueError, "changed"):
                patching.apply_patch(packet, proposed, dry_run=True)

    def test_read_only_review_packet_rejects_preview(self):
        with tempfile.TemporaryDirectory() as folder:
            paper = Path(folder) / "paper.md"
            paper.write_text("# Methods\nNo edit.\n", encoding="utf-8")
            inventory = patching.inspect_manuscript(paper)
            packet = {"schema_version": 1, "operation": "review",
                      "manuscript": {"path": str(paper), "version": inventory["version"]},
                      "targets": ["methods"], "dependencies": []}
            with self.assertRaisesRegex(ValueError, "read-only"):
                patching.apply_patch(packet, {"base_version": inventory["version"], "edits": []},
                                     dry_run=True)


if __name__ == "__main__":
    unittest.main()
