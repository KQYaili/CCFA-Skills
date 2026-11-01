#!/usr/bin/env python3
"""Unit tests for project figure-registry checks."""
from __future__ import annotations

import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_figure_registry import check_registry


class FigureRegistryChecks(unittest.TestCase):
    def setUp(self):
        self.figures = {
            "version": 1,
            "project": "Demo",
            "figures": [
                {"id": "fig:main-results", "kind": "quantitative", "status": "reserved",
                 "section": "Experiments", "purpose": "Compare methods", "evidence_paths": [],
                 "protocol_id": None, "method_frozen": False, "in_manuscript": True},
                {"id": "fig:method-overview", "kind": "architecture", "status": "reserved",
                 "section": "Method", "purpose": "Show computation", "evidence_paths": [],
                 "protocol_id": None, "method_frozen": False, "in_manuscript": True},
            ]
        }
        self.tex = r"\begin{figure}\caption{Draft}\label{fig:main-results}\end{figure}" + "\n" + \
                   r"\begin{figure}\caption{Draft}\label{fig:method-overview}\end{figure}" + "\n" + \
                   r"As shown in Fig.~\ref{fig:main-results} and \cref{fig:method-overview}."

    def test_pending_manuscript_may_have_reserved_figures(self):
        self.assertEqual(check_registry(self.figures, tex_sources=[self.tex]), [])

    def test_submission_rejects_pending_figures(self):
        problems = check_registry(self.figures, tex_sources=[self.tex], submission=True)
        self.assertTrue(any("not final" in e for e in problems))

    def test_verified_quantitative_requires_protocol_and_evidence(self):
        self.figures["figures"][0]["status"] = "verified"
        problems = check_registry(self.figures)
        self.assertTrue(any("protocol_id" in e for e in problems))
        self.assertTrue(any("evidence_paths" in e for e in problems))
        self.figures["figures"][0]["protocol_id"] = "protocol-v1"
        self.figures["figures"][0]["evidence_paths"] = ["results/run-1.json"]
        self.assertEqual(check_registry(self.figures), [])

    def test_final_architecture_requires_freeze(self):
        self.figures["figures"][1]["status"] = "final"
        self.figures["figures"][1]["evidence_paths"] = ["figures/method.svg"]
        self.assertTrue(any("method_frozen" in e for e in check_registry(self.figures)))
        self.figures["figures"][1]["method_frozen"] = True
        self.assertEqual(check_registry(self.figures), [])

    def test_figure_references_and_registry_must_match(self):
        broken = self.tex.replace(r"\label{fig:method-overview}", "")
        problems = check_registry(self.figures, tex_sources=[broken])
        self.assertTrue(any("missing LaTeX label" in e for e in problems))
        unknown = self.tex + r" More \ref{fig:unknown}."
        self.assertTrue(any("not registered" in e for e in check_registry(self.figures, tex_sources=[unknown])))

    def test_commented_labels_do_not_count(self):
        broken = self.tex.replace(r"\label{fig:method-overview}", r"% \label{fig:method-overview}")
        problems = check_registry(self.figures, tex_sources=[broken])
        self.assertTrue(any("missing LaTeX label" in e for e in problems))

    def test_submission_draft_marker_fails(self):
        self.figures["figures"][0].update(status="final", protocol_id="p1", evidence_paths=["results/data.csv"])
        self.figures["figures"][1].update(status="final", method_frozen=True, evidence_paths=["figures/method.svg"])
        self.assertEqual(check_registry(self.figures, tex_sources=[self.tex], submission=True), [])
        errors = check_registry(self.figures, tex_sources=[self.tex + "\n% DRAFT FIGURE SLOT"], submission=True)
        self.assertTrue(any("draft figure marker" in e for e in errors))

    def test_duplicate_id_and_path_traversal_fail(self):
        fig = copy.deepcopy(self.figures["figures"][0]); fig["id"] = "fig:method-overview"
        fig["evidence_paths"] = ["../secrets"]
        self.figures["figures"].append(fig)
        errors = check_registry(self.figures)
        self.assertTrue(any("duplicate figure ID" in e for e in errors))
        self.assertTrue(any("relative" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
