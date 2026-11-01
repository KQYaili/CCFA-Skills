#!/usr/bin/env python3
"""Check a CCFA research figure registry and optional manuscript labels.

This is a structural gate, NOT validation of scientific evidence or artwork.
Requires Python 3.10+, standard library only. No files are modified.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

KINDS = {"quantitative", "architecture", "workflow", "other"}
STATES = {"reserved", "exploratory", "verified", "final"}
FIG_ID = re.compile(r"^fig:[a-z0-9][a-z0-9-]*$")
LATEX_CMD = re.compile(r"\\(?:label|(?:[Cc]ref|ref|autoref|eqref)\*?)\s*(?:\[[^]]*\])?\s*\{([^}]+)\}")
DRAFT_MARKER = re.compile(r"DRAFT FIGURE SLOT|FIGURE PENDING", re.IGNORECASE)


def _unique_pairs(items: list[tuple[str, object]]) -> dict[str, object]:
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_registry(path: Path) -> dict:
    with path.open(encoding="utf-8-sig") as stream:
        data = json.load(stream, object_pairs_hook=_unique_pairs,
                         parse_constant=lambda x: (_ for _ in ()).throw(ValueError(f"invalid number: {x}")))
    if not isinstance(data, dict):
        raise ValueError("registry must be a JSON object")
    return data


def check_registry(registry: dict, *, tex_sources: list[str] | None = None,
                   submission: bool = False) -> list[str]:
    errors: list[str] = []
    if type(registry.get("version")) is not int or registry["version"] != 1:
        errors.append("registry.version must be integer 1")
    if not isinstance(registry.get("project"), str) or not registry["project"].strip():
        errors.append("registry.project must be nonempty text")
    figures = registry.get("figures")
    if not isinstance(figures, list):
        return errors + ["registry.figures must be a list"]

    seen: set[str] = set()
    expected_labels: set[str] = set()
    for index, fig in enumerate(figures):
        loc = f"figures[{index}]"
        if not isinstance(fig, dict):
            errors.append(f"{loc} must be an object")
            continue
        figure_id = fig.get("id")
        if not isinstance(figure_id, str) or not FIG_ID.fullmatch(figure_id):
            errors.append(f"{loc}.id must be fig:<lowercase-hyphen-key>")
        elif figure_id in seen:
            errors.append(f"duplicate figure ID: {figure_id}")
        else:
            seen.add(figure_id)
        if fig.get("kind") not in KINDS:
            errors.append(f"{loc}.kind must be one of {sorted(KINDS)}")
        if fig.get("status") not in STATES:
            errors.append(f"{loc}.status must be one of {sorted(STATES)}")
        for field in ("section", "purpose"):
            if not isinstance(fig.get(field), str) or not fig[field].strip():
                errors.append(f"{loc}.{field} must be nonempty text")
        evidence = fig.get("evidence_paths")
        if not isinstance(evidence, list) or any(not isinstance(p, str) or not p.strip() for p in evidence):
            errors.append(f"{loc}.evidence_paths must be a list of nonempty paths")
            evidence = []
        for path in evidence:
            normalized = path.replace("\\", "/")
            if normalized.startswith("/") or re.match(r"^[a-zA-Z]:/", normalized) or ".." in normalized.split("/"):
                errors.append(f"{loc}.evidence_paths must be relative to the project, without '..'")
        if type(fig.get("method_frozen")) is not bool:
            errors.append(f"{loc}.method_frozen must be boolean")
        if type(fig.get("in_manuscript")) is not bool:
            errors.append(f"{loc}.in_manuscript must be boolean")
        if fig.get("in_manuscript") is True and isinstance(figure_id, str) and FIG_ID.fullmatch(figure_id):
            expected_labels.add(figure_id)
        if fig.get("status") in ("verified", "final"):
            if not evidence:
                errors.append(f"{loc} verified/final figures need evidence_paths")
            if fig.get("kind") == "quantitative" and not (isinstance(fig.get("protocol_id"), str) and fig["protocol_id"].strip()):
                errors.append(f"{loc} verified/final quantitative figure needs protocol_id")
            if fig.get("kind") in ("architecture", "workflow") and fig.get("method_frozen") is not True:
                errors.append(f"{loc} verified/final method diagram needs method_frozen=true")
        if submission and fig.get("in_manuscript") is True and fig.get("status") != "final":
            errors.append(f"{loc} is referenced by the planned manuscript but not final")

    if tex_sources is not None:
        all_labels: set[str] = set()
        all_references: set[str] = set()
        for tex in tex_sources:
            if DRAFT_MARKER.search(tex):
                if submission:
                    errors.append("draft figure marker remains in submission TeX")
            active_tex = "\n".join(re.sub(r"(?<!\\)%.*$", "", line) for line in tex.splitlines())
            for match in LATEX_CMD.finditer(active_tex):
                key = match.group(1)
                command = active_tex[match.start():match.start() + 20]
                keys = [k.strip() for k in key.split(",")]
                if command.startswith("\\label"):
                    all_labels.update(k for k in keys if k.startswith("fig:"))
                else:
                    all_references.update(k for k in keys if k.startswith("fig:"))
        for key in sorted(all_references - seen):
            errors.append(f"TeX reference not registered: {key}")
        for key in sorted(all_references - all_labels):
            errors.append(f"TeX reference missing LaTeX label: {key}")
        for key in sorted(expected_labels - all_labels):
            errors.append(f"registry in_manuscript figure missing LaTeX label: {key}")
        for key in sorted(all_labels - seen):
            errors.append(f"LaTeX figure label not registered: {key}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("registry", type=Path)
    parser.add_argument("--tex", type=Path, action="append", default=[],
                        help="A .tex file from the full manuscript, repeat as needed")
    parser.add_argument("--submission", action="store_true", help="Require all included figures to be final and no draft markers")
    args = parser.parse_args(argv)
    try:
        data = load_registry(args.registry)
        tex = [path.read_text(encoding="utf-8-sig") for path in args.tex] if args.tex else None
        errors = check_registry(data, tex_sources=tex, submission=args.submission)
    except (OSError, ValueError, UnicodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"FAIL: {len(errors)} issue(s)", file=sys.stderr)
        return 1
    print(f"OK: {len(data['figures'])} figure(s) passed structural checks; scientific fidelity not assessed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
