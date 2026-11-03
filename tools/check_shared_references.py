#!/usr/bin/env python3
"""Shared-reference integrity checker for CCFA (pointer architecture).

Provenance: adapted from HKUSTDial/Supervisor-Skills,
`scripts/check_shared_sync.py` (CC BY-NC-SA 4.0, Copyright (c) 2026
Yuyu Luo). The source checker guards a COPY architecture: shared files
are duplicated per skill and must stay byte-identical to a canonical
copy. CCFA does not copy shared references — skills consume
`ccf-common/references/*.md` through relative-path pointers (Markdown
links and the frontmatter `metadata.ccf_skill_controls.shared_controls`
declaration). The meaningful invariant for a pointer architecture is
therefore different, and this checker enforces that instead:

 1. Canonical targets exist: every relative Markdown link in any skill
    file whose target resolves into `ccf-common/references/` points at
    an existing file (no dangling shared pointers).
 2. Declared control roots resolve: each SKILL.md's
    `metadata.ccf_skill_controls.shared_controls` value, when present,
    resolves to an existing directory.
 3. No shadow copies: no file outside `ccf-common/references/` is
    byte-identical to a shared reference — a copied fork of a shared
    file is the drift hazard this check exists to catch. (Same-basename
    files with different content and roles exist legitimately, e.g.
    `ccf-a-venue-map.md`, and are not flagged.)

Shared references never pointed to from any Markdown file in the repo
are listed as information only; they may be entry points referenced from
outside the tree.

Exit 0 when all checks pass, 1 on any violation. Prints one line per
violation.
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

MD_LINK = re.compile(r"\[[^\]]+\]\(([^)\s]+)(?:\s+[^)]*)?\)")
SKIP_DIRS = {".git", "ccfa-workfiles", "node_modules", "__pycache__"}


def iter_markdown(root: Path):
    for path in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        yield path


def frontmatter(text: str) -> dict | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---\n", 4)
    if end == -1:
        return None
    try:
        parsed = yaml.safe_load(text[4:end])
    except yaml.YAMLError:
        return None
    return parsed if isinstance(parsed, dict) else None


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    common_refs_dir = (repo_root / "ccf-common" / "references").resolve()
    errors: list[str] = []

    if not common_refs_dir.is_dir():
        print("shared-references: ccf-common/references/ missing; nothing to check.")
        return 1

    shared_files = {p.resolve() for p in common_refs_dir.glob("*.md")}
    shared_bytes = {}
    for p in shared_files:
        shared_bytes.setdefault(p.read_bytes(), p)

    pointed_to: set[Path] = set()
    skill_dirs = [
        p for p in sorted(repo_root.iterdir()) if p.is_dir() and (p / "SKILL.md").exists()
    ]

    for md in iter_markdown(repo_root):
        try:
            text = md.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for m in MD_LINK.finditer(text):
            target = m.group(1).strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            target = target.split("#", 1)[0]
            if not target.endswith(".md"):
                continue
            resolved = (md.parent / target).resolve()
            if resolved.parent == common_refs_dir or common_refs_dir in resolved.parents:
                pointed_to.add(resolved)
                if resolved not in shared_files and not resolved.exists():
                    errors.append(
                        f"{md.relative_to(repo_root)}: dangling shared pointer -> {target}"
                    )
        # Shadow-copy scan: byte-identical copies of shared references.
        resolved_md = md.resolve()
        if common_refs_dir not in resolved_md.parents and resolved_md not in shared_files:
            canonical = shared_bytes.get(md.read_bytes())
            if canonical is not None:
                errors.append(
                    f"{md.relative_to(repo_root)}: byte-identical shadow copy of "
                    f"shared reference {canonical.relative_to(repo_root)}; "
                    "point to the canonical file instead of copying it"
                )

    for skill_dir in skill_dirs:
        skill_md = skill_dir / "SKILL.md"
        fm = frontmatter(skill_md.read_text(encoding="utf-8"))
        if fm is None:
            continue
        controls = (fm.get("metadata") or {}).get("ccf_skill_controls") or {}
        shared_controls = controls.get("shared_controls")
        if isinstance(shared_controls, str):
            target = (skill_dir / shared_controls).resolve()
            if not target.is_dir():
                errors.append(
                    f"{skill_md.relative_to(repo_root)}: shared_controls "
                    f"{shared_controls!r} does not resolve to a directory"
                )

    if errors:
        print(f"shared-references: {len(errors)} violation(s)")
        for e in errors:
            print(f"  {e}")
        return 1

    orphans = sorted(p.name for p in shared_files if p not in pointed_to)
    print(
        f"shared-references: {len(shared_files)} canonical file(s), "
        f"{len(pointed_to & shared_files)} pointed to, all pointers resolve, "
        "no shadow copies"
    )
    if orphans:
        print(f"shared-references: info — never pointed to in-repo: {', '.join(orphans)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
