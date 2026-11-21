"""Verify the CVPR 2027 author kit files or identify a project's style."""

import argparse
import hashlib
import json
from pathlib import Path
import sys


KIT = Path(__file__).resolve().parents[2] / "ccf-latex-templates" / "CVPR" / "2027"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--kit", type=Path, help="compare a pristine copy to the conference archive")
    group.add_argument("--style", type=Path, help="identify the selected cvpr.sty by its exact bytes")
    args = parser.parse_args(argv)
    try:
        manifest = json.loads((KIT / "template-source.json").read_text(encoding="utf-8"))
        files = {row["path"]: row["sha256"] for row in manifest["files"]}
        if args.style is not None:
            sources = {files["cvpr.sty"]: "conference-linked archive"}
            sources.update({row["sha256"]: row["source"] for row in manifest["equivalent_styles"]})
            source = sources.get(digest(args.style))
            if source is None:
                print("Style differs from both recorded official variants.")
                return 1
            print(f"CVPR 2027 v1 style matches the {source}.")
            return 0

        root = args.kit or KIT
        differences = [name for name, expected in files.items()
                       if not (root / name).is_file() or digest(root / name) != expected]
        if differences:
            print("Missing or different template files:", ", ".join(differences))
            return 1
        print(f"All {len(files)} conference archive files match.")
        return 0
    except (OSError, ValueError, KeyError) as error:
        print(f"Could not verify template: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
