#!/usr/bin/env python3
"""Structural linter for CCFA SKILL.md files.

Provenance: adapted from HKUSTDial/Supervisor-Skills,
`scripts/lint_skills.py` (CC BY-NC-SA 4.0, Copyright (c) 2026 Yuyu Luo).
The checking machinery (frontmatter parsing, pointer resolution, one line
per violation, exit 0/1) is carried over; the RULE SET is re-derived from
CCFA's own documented conventions, not the source repo's house rules.

Enforced (CCFA conventions):
 - SKILL.md frontmatter parses as a YAML mapping
 - frontmatter `name` is kebab-case and equals the directory name
 - `description` is present and non-empty; specialist skills carry a
   "Use for" / "Use when" trigger clause (CCFA descriptions are long
   trigger-style texts, often with CJK trigger terms — no word-count,
   person, CJK, or punctuation rules apply). The two family preflight
   skills (ccf-common, ccf-humanization) are exempt from the trigger
   clause: every other skill loads them unconditionally by contract.
 - every relative Markdown link in the SKILL.md body ending in .md
   resolves to an existing file (reference pointers must not dangle)
 - references/*.md files are valid UTF-8

Deliberately NOT enforced (source-repo house rules with no CCFA basis):
 - 40..80-word third-person descriptions, em-dash ban, CJK ban,
   banned-attribution strings, table-of-contents rule
 - "no nested references": CCFA reference files cross-link by design
   (shared ccf-common pointers, index hubs, sibling references); link
   *resolution* is enforced here and repo-wide by
   ccf-common/scripts/check_markdown_links.py instead
 - a SKILL.md body line cap: no CCFA document sets one (all bodies are
   currently <= 100 lines); re-derive a cap from
   ccf-common/references/skill-maintenance.md before adding one

Exit 0 on clean, 1 on any violation. Prints one line per violation.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError as exc:
    raise SystemExit(
        "PyYAML is required; install pyyaml (see .github/workflows/validate.yml)"
    ) from exc

# Skills loaded unconditionally as family preflights; their descriptions
# state a contract role rather than trigger conditions.
PREFLIGHT_SKILLS = {"ccf-common", "ccf-humanization"}

MD_LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)(?:\s+[^)]*)?\)")
NAME_RE = re.compile(r"[a-z0-9][a-z0-9\-]{0,62}[a-z0-9]")


def parse_frontmatter(text: str) -> tuple[dict[str, object], str]:
    """Return (frontmatter dict, body). Raises ValueError on malformed."""
    if not text.startswith("---\n"):
        raise ValueError("missing YAML frontmatter opener '---'")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise ValueError("missing YAML frontmatter closer '---'")
    fm_text = text[4:end]
    body = text[end + 5 :]
    try:
        parsed = yaml.safe_load(fm_text)
    except yaml.YAMLError as exc:
        problem = getattr(exc, "problem", None) or str(exc)
        mark = getattr(exc, "problem_mark", None)
        location = f" at line {mark.line + 1}, column {mark.column + 1}" if mark else ""
        raise ValueError(f"invalid YAML frontmatter{location}: {problem}") from exc
    if not isinstance(parsed, dict):
        raise ValueError("YAML frontmatter must be a mapping")
    if not all(isinstance(key, str) for key in parsed):
        raise ValueError("YAML frontmatter keys must be strings")
    return parsed, body


def check_description(skill_name: str, desc: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(desc, str) or not desc.strip():
        errors.append("frontmatter 'description' must be a non-empty string")
        return errors
    if skill_name not in PREFLIGHT_SKILLS:
        if "Use for" not in desc and "Use when" not in desc:
            errors.append(
                "description has no 'Use for'/'Use when' trigger clause "
                "(CCFA trigger-style convention)"
            )
    return errors


def check_pointers(skill_dir: Path, body: str) -> list[str]:
    errors: list[str] = []
    seen: set[str] = set()
    for m in MD_LINK.finditer(body):
        target = m.group(1).strip("<>")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target = target.split("#", 1)[0]
        if not target.endswith(".md") or target in seen:
            continue
        seen.add(target)
        if not (skill_dir / target).resolve().exists():
            errors.append(f"pointer to missing file: {target}")
    return errors


def lint_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.exists():
        return [f"{skill_dir}: missing SKILL.md"]

    try:
        text = skill_md.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return [f"{skill_md}: not valid UTF-8"]

    try:
        fm, body = parse_frontmatter(text)
    except ValueError as e:
        return [f"{skill_md}: {e}"]

    name = fm.get("name")
    if not isinstance(name, str):
        errors.append(f"{skill_md}: frontmatter 'name' must be a string")
    else:
        if not NAME_RE.fullmatch(name):
            errors.append(f"{skill_md}: name {name!r} must be kebab-case, 2..64 chars, [a-z0-9-]")
        if name != skill_dir.name:
            errors.append(
                f"{skill_md}: frontmatter name {name!r} must match directory name {skill_dir.name!r}"
            )

    if "description" not in fm:
        errors.append(f"{skill_md}: frontmatter missing 'description'")
    else:
        errors.extend(f"{skill_md}: {e}" for e in check_description(skill_dir.name, fm["description"]))

    errors.extend(f"{skill_md}: {e}" for e in check_pointers(skill_dir, body))

    ref_dir = skill_dir / "references"
    if ref_dir.is_dir():
        for ref_md in sorted(ref_dir.rglob("*.md")):
            try:
                ref_md.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                errors.append(f"{ref_md}: not valid UTF-8")
    return errors


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    skill_dirs = [
        p for p in sorted(repo_root.iterdir()) if p.is_dir() and (p / "SKILL.md").exists()
    ]
    if not skill_dirs:
        print("lint: no skills found; nothing to lint.")
        return 0

    all_errors: list[str] = []
    for skill_dir in skill_dirs:
        all_errors.extend(lint_skill(skill_dir))

    if all_errors:
        print(f"lint: {len(all_errors)} violation(s)")
        for e in all_errors:
            print(f"  {e}")
        return 1

    print(f"lint: {len(skill_dirs)} skill(s) clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
