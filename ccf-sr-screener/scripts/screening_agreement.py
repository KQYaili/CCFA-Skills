#!/usr/bin/env python3
"""Inter-screener agreement statistics for dual-blind screening.

Original CCFA code, written for ccf-sr-screener; no third-party source.
Computes observed agreement, Cohen's kappa, and PABAK (prevalence- and
bias-adjusted kappa) from two screeners' decision files, and lists every
record the two screeners decided differently so it can be routed to
adjudication. Kappa alone is misleading when one decision dominates
(the usual case in screening, where most records are excluded), so the
report always carries all three numbers; see
../references/agreement-statistics.md for definitions and reading rules.

Input: two CSV files, each with a header row containing at least the
columns `record_id` and `decision`. Decisions are `include` or
`exclude` (case-insensitive). A decision of `pending` (or an empty cell)
means the screener never produced a verdict for that record: such
records are counted and reported, never silently treated as `exclude`,
and are left out of the agreement statistics.

Usage:
    python screening_agreement.py A.csv B.csv [--format text|json]
    python screening_agreement.py --self-test
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

DECISIONS = {"include", "exclude"}
UNRATED = {"pending", ""}


def load_decisions(path: Path) -> dict[str, str]:
    """Read one screener's CSV into {record_id: decision-or-'pending'}."""
    text = path.read_text(encoding="utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    if reader.fieldnames is None:
        raise ValueError(f"{path}: missing CSV header row")
    fields = {name.strip().lower(): name for name in reader.fieldnames if name}
    for required in ("record_id", "decision"):
        if required not in fields:
            raise ValueError(f"{path}: CSV must contain a '{required}' column")
    decisions: dict[str, str] = {}
    for row in reader:
        record_id = (row.get(fields["record_id"]) or "").strip()
        if not record_id:
            continue
        raw = (row.get(fields["decision"]) or "").strip().lower()
        if raw in UNRATED:
            decisions[record_id] = "pending"
        elif raw in DECISIONS:
            decisions[record_id] = raw
        else:
            raise ValueError(
                f"{path}: record {record_id!r} has unknown decision {raw!r}; "
                "expected include, exclude, or pending"
            )
    return decisions


def agreement(a: dict[str, str], b: dict[str, str]) -> dict:
    """Agreement statistics over records both screeners actually rated."""
    shared = sorted(set(a) & set(b))
    rated = [r for r in shared if a[r] != "pending" and b[r] != "pending"]
    unrated = [r for r in shared if a[r] == "pending" or b[r] == "pending"]
    only_a = sorted(set(a) - set(b))
    only_b = sorted(set(b) - set(a))

    both_include = sum(1 for r in rated if a[r] == b[r] == "include")
    both_exclude = sum(1 for r in rated if a[r] == b[r] == "exclude")
    a_include_b_exclude = sum(
        1 for r in rated if a[r] == "include" and b[r] == "exclude"
    )
    a_exclude_b_include = sum(
        1 for r in rated if a[r] == "exclude" and b[r] == "include"
    )
    disagreements = [
        r for r in rated if a[r] != b[r]
    ]

    n = len(rated)
    result: dict = {
        "records_in_a": len(a),
        "records_in_b": len(b),
        "records_in_both": len(shared),
        "records_rated_by_both": n,
        "unrated_by_either": len(unrated),
        "only_in_a": only_a,
        "only_in_b": only_b,
        "both_include": both_include,
        "both_exclude": both_exclude,
        "a_include_b_exclude": a_include_b_exclude,
        "a_exclude_b_include": a_exclude_b_include,
        "disagreement_ids": disagreements,
    }
    if n == 0:
        result.update(
            observed_agreement=None, cohens_kappa=None, pabak=None,
            note="no records rated by both screeners; statistics undefined",
        )
        return result

    po = (both_include + both_exclude) / n
    a_include = both_include + a_include_b_exclude
    b_include = both_include + a_exclude_b_include
    pe = (a_include * b_include + (n - a_include) * (n - b_include)) / (n * n)
    kappa = None if pe >= 1.0 else (po - pe) / (1.0 - pe)
    result.update(
        observed_agreement=round(po, 6),
        cohens_kappa=None if kappa is None else round(kappa, 6),
        pabak=round(2.0 * po - 1.0, 6),
        expected_agreement=round(pe, 6),
    )
    return result


def to_text(result: dict, name_a: str, name_b: str) -> str:
    lines = [
        "Screening agreement report",
        f"- Screener A: {name_a} ({result['records_in_a']} records)",
        f"- Screener B: {name_b} ({result['records_in_b']} records)",
        f"- Records in both files: {result['records_in_both']}",
        f"- Records rated by both: {result['records_rated_by_both']}",
        f"- Unrated by either (never defaulted): {result['unrated_by_either']}",
        f"- Both include: {result['both_include']}",
        f"- Both exclude: {result['both_exclude']}",
        f"- A include / B exclude: {result['a_include_b_exclude']}",
        f"- A exclude / B include: {result['a_exclude_b_include']}",
    ]
    if result["observed_agreement"] is not None:
        lines += [
            f"- Observed agreement: {result['observed_agreement']:.4f}",
            f"- Cohen's kappa: {result['cohens_kappa']}",
            f"- PABAK: {result['pabak']:.4f}",
        ]
    if result.get("note"):
        lines.append(f"- Note: {result['note']}")
    if result["disagreement_ids"]:
        lines.append(
            "- Disagreements routed to adjudication: "
            + ", ".join(result["disagreement_ids"])
        )
    if result["only_in_a"] or result["only_in_b"]:
        lines.append(
            f"- Only in A: {result['only_in_a']}; only in B: {result['only_in_b']}"
        )
    return "\n".join(lines) + "\n"


def self_test() -> int:
    a = {
        "r01": "include", "r02": "include", "r03": "include",
        "r04": "exclude", "r05": "exclude", "r06": "exclude",
        "r07": "exclude", "r08": "exclude",
        "r09": "include", "r10": "exclude", "r11": "pending",
    }
    b = {
        "r01": "include", "r02": "include", "r03": "include",
        "r04": "exclude", "r05": "exclude", "r06": "exclude",
        "r07": "exclude", "r08": "exclude",
        "r09": "exclude", "r10": "include", "r11": "exclude",
    }
    result = agreement(a, b)
    assert result["records_rated_by_both"] == 10, result
    assert result["both_include"] == 3 and result["both_exclude"] == 5, result
    assert result["unrated_by_either"] == 1, result
    assert abs(result["observed_agreement"] - 0.8) < 1e-9, result
    # Pe = (4*4 + 6*6)/100 = 0.52; kappa = (0.8-0.52)/(1-0.52) = 0.583333...
    assert abs(result["cohens_kappa"] - 0.583333) < 1e-6, result
    assert abs(result["pabak"] - 0.6) < 1e-9, result
    assert result["disagreement_ids"] == ["r09", "r10"], result
    print("self-test OK: agreement=0.8000 kappa=0.583333 pabak=0.6000")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("file_a", nargs="?", type=Path)
    parser.add_argument("file_b", nargs="?", type=Path)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        return self_test()
    if not args.file_a or not args.file_b:
        parser.error("two decision CSV files are required (or --self-test)")
    try:
        decisions_a = load_decisions(args.file_a)
        decisions_b = load_decisions(args.file_b)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    result = agreement(decisions_a, decisions_b)
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(to_text(result, str(args.file_a), str(args.file_b)), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
