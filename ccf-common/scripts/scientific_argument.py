#!/usr/bin/env python3
"""Validate optional per-paper scientific argument state or export a writer brief.

No paper, ccfa.yaml, preference, or experimental record is modified by validate/brief.
"""
import argparse
import json
from pathlib import Path
from readable_versions import file_stamp
import sys

RECORD = "ccfa-scientific-argument"
STAGES = {"unassessed", "exploratory", "confirmatory", "theoretical"}
STATES = {"todo", "draft", "review", "frozen", "verified"}


def need(condition, message):
    if not condition:
        raise ValueError(message)


def obj(value, name):
    need(isinstance(value, dict), name + " must be an object")
    return value


def string(value, name, nonempty=False):
    need(isinstance(value, str) and (not nonempty or bool(value.strip())),
         name + " must be a " + ("nonempty " if nonempty else "") + "string")
    return value


def unique(items, label):
    need(isinstance(items, list), label + " must be a list")
    seen = set()
    for item in items:
        obj(item, label + " entry")
        key = string(item.get("id"), label + ".id", nonempty=True)
        need(key not in seen, "duplicate " + label + " id: " + key)
        seen.add(key)


def validate(data, manuscript=None):
    obj(data, "state")
    need(data.get("record_type") == RECORD, "wrong record_type")
    need(type(data.get("schema_version")) is int and data["schema_version"] == 1,
         "schema_version must be 1")
    string(data.get("paper_id"), "paper_id", nonempty=True)
    question = string(data.get("scientific_question"), "scientific_question")
    throughline = string(data.get("throughline"), "throughline")
    hypotheses = data.get("hypotheses")
    paragraphs = data.get("paragraphs")
    unique(hypotheses, "hypotheses")
    unique(paragraphs, "paragraphs")
    pending = []
    for item in hypotheses:
        ident = item["id"]
        for field in ("statement", "rival", "prediction"):
            string(item.get(field), "hypothesis " + ident + "." + field)
            if not item[field].strip():
                pending.append(ident + "." + field)
        need(item.get("evidence_stage") in STAGES,
             "invalid evidence_stage for " + ident)
        refs = item.get("evidence_refs")
        need(isinstance(refs, list) and all(isinstance(x, str) and x.strip() for x in refs),
             "evidence_refs must be a list of nonempty source anchors: " + ident)
    current_version = None
    if manuscript is not None:
        path = Path(manuscript)
        need(path.is_file(), "manuscript not found: " + str(path))
        current_version = file_stamp(path)
    for item in paragraphs:
        ident = item["id"]
        string(item.get("section_id"), "paragraph " + ident + ".section_id", nonempty=True)
        need(item.get("status") in STATES, "invalid paragraph status: " + ident)
        source_version = item.get("manuscript_version")
        need(source_version is None or (isinstance(source_version, str) and source_version.strip()),
             "invalid manuscript_version: " + ident)
        if item["status"] == "verified":
            need(source_version is not None, "verified paragraph requires manuscript_version: " + ident)
            receipt = obj(item.get("verification"), "verification for " + ident)
            string(receipt.get("scope"), "verification.scope for " + ident, nonempty=True)
            string(receipt.get("receipt"), "verification.receipt for " + ident, nonempty=True)
            if current_version is not None:
                need(current_version == source_version, "verified paragraph is stale: " + ident)
    return {"valid": True, "paper_id": data["paper_id"],
            "ready_for_brief": bool(question.strip() and throughline.strip()),
            "hypotheses": len(hypotheses), "paragraphs": len(paragraphs),
            "unfilled_hypothesis_fields": pending,
            "verification_version_checked": current_version is not None}


def example(paper_id):
    return {"record_type": RECORD, "schema_version": 1, "paper_id": paper_id,
            "scientific_question": "", "throughline": "",
            "hypotheses": [], "paragraphs": []}


def cli(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    init = commands.add_parser("init", help="Create blank state without overwriting an existing file")
    init.add_argument("--file", required=True)
    init.add_argument("--paper-id", required=True)
    check = commands.add_parser("validate", help="Structural audit; optional readable manuscript version check")
    check.add_argument("--file", required=True)
    check.add_argument("--manuscript")
    brief = commands.add_parser("brief", help="Print a compatible writing_runtime --brief JSON object")
    brief.add_argument("--file", required=True)
    args = parser.parse_args(argv)
    if args.command == "init":
        string(args.paper_id, "paper_id", nonempty=True)
        dest = Path(args.file).absolute()
        need(dest.suffix == ".json" and dest.parent.is_dir(), "use a .json file under an existing directory")
        need(not dest.is_symlink(), "refuse symlink output")
        with dest.open("x", encoding="utf-8", newline="\n") as fp:
            json.dump(example(args.paper_id), fp, ensure_ascii=False, indent=2)
            fp.write("\n")
        return {"created": str(dest)}
    data = json.loads(Path(args.file).read_text(encoding="utf-8-sig"))
    report = validate(data, getattr(args, "manuscript", None))
    if args.command == "validate":
        return report
    need(report["ready_for_brief"], "scientific question and throughline must be filled before brief export")
    return {"message": data["scientific_question"], "throughline": data["throughline"]}


def main():
    try:
        result = cli()
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
