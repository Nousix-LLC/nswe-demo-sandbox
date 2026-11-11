#!/usr/bin/env python3
"""Parse the chirp release bar into (bar_id, stage, verification_method, [REQ refs]),
build the inverted REQ -> bar_ids map, and evaluate the BAR_TESTABLE identity.

Reads the release-bar.md path given as argv[1]. Emits a structured report to stdout.
No file is written by this script; the agent composes the deliverable from this report.

Authoritative field source per the subtree contract:
  - line shape: **BAR-NNN** (`stage` · `method`) — statement _Enforces REQ-*, REQ-*._
  - the REQ references are the trailing italic `_Enforces ... ._` clause ONLY (not prose).
  - closed verification_method vocabulary and stage values are the inherited schema's.
"""
import re
import sys
import json
from collections import defaultdict

VERIF_VOCAB = {"manual_user_check", "automated_test", "inspection", "operational_check"}
STAGE_VOCAB = {"usable_early", "releasable"}

# A criterion line begins at column 0 with **BAR-NNN**.
BAR_LINE = re.compile(r"^\*\*BAR-(\d+)\*\*\s*\((.*?)\)\s*[—-]\s*(.*)$")
# The header inside the parens: `stage` · `method`  (backtick-quoted, middot-separated)
HEADER = re.compile(r"`([^`]+)`\s*·\s*`([^`]+)`")
# The authoritative references clause: the trailing _Enforces ... ._ italic run.
ENFORCES = re.compile(r"_Enforces\s+(.*?)\._\s*$")
REQ_ID = re.compile(r"REQ-[A-Z]+-\d+")


def main():
    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as fh:
        lines = fh.readlines()

    records = []          # list of dicts: id_str, num, stage, method, reqs(list), raw issues
    seen_ids = {}         # id_str -> first line number, to catch duplicates
    parse_problems = []   # lines that look like a BAR but did not fully parse

    for lineno, line in enumerate(lines, 1):
        line = line.rstrip("\n")
        if not line.startswith("**BAR-"):
            continue
        m = BAR_LINE.match(line)
        if not m:
            parse_problems.append((lineno, "unrecognized BAR line shape", line[:120]))
            continue
        num = int(m.group(1))
        id_str = f"BAR-{m.group(1)}"
        header = m.group(2)
        body = m.group(3)

        hm = HEADER.search(header)
        if hm:
            stage = hm.group(1).strip()
            method = hm.group(2).strip()
        else:
            stage = None
            method = None
            parse_problems.append((lineno, "could not parse (stage · method) header", header[:120]))

        em = ENFORCES.search(body)
        if em:
            reqs = REQ_ID.findall(em.group(1))
        else:
            reqs = []
            parse_problems.append((lineno, "no trailing _Enforces ..._ clause", body[-80:]))
        # de-duplicate while preserving order
        seen = set()
        reqs_dedup = [r for r in reqs if not (r in seen or seen.add(r))]

        if id_str in seen_ids:
            parse_problems.append((lineno, f"duplicate {id_str} (first at line {seen_ids[id_str]})", ""))
        else:
            seen_ids[id_str] = lineno

        records.append({
            "id": id_str,
            "num": num,
            "lineno": lineno,
            "stage": stage,
            "method": method,
            "reqs": reqs_dedup,
        })

    records.sort(key=lambda r: r["num"])

    # ---- Stage / area breakdowns (cross-check against the bar's own header table) ----
    def area_of(num):
        if 1 <= num <= 99:
            return "Product"
        if 100 <= num <= 199:
            return "Domain & application"
        if 200 <= num <= 299:
            return "Experience"
        if 300 <= num <= 399:
            return "Identity, security & trust"
        if 400 <= num <= 499:
            return "Operational readiness"
        return "UNKNOWN-RANGE"

    stage_counts = defaultdict(int)
    area_counts = defaultdict(lambda: defaultdict(int))
    for r in records:
        stage_counts[r["stage"]] += 1
        area_counts[area_of(r["num"])][r["stage"]] += 1

    # ---- Inversion REQ -> sorted bar_ids ----
    inv = defaultdict(list)
    for r in records:
        for q in r["reqs"]:
            inv[q].append(r["id"])

    def req_sort_key(q):
        m = re.match(r"REQ-([A-Z]+)-(\d+)", q)
        return (m.group(1), int(m.group(2))) if m else (q, 0)

    def bar_sort_key(b):
        return int(b.split("-")[1])

    inv_sorted = {q: sorted(set(inv[q]), key=bar_sort_key) for q in sorted(inv, key=req_sort_key)}

    # ---- BAR_TESTABLE evaluation ----
    offenders = []
    for r in records:
        bad_method = r["method"] not in VERIF_VOCAB
        no_req = len(r["reqs"]) == 0
        bad_stage = r["stage"] not in STAGE_VOCAB
        if bad_method or no_req or bad_stage:
            reasons = []
            if bad_method:
                reasons.append(f"verification_method {r['method']!r} not in closed vocabulary")
            if no_req:
                reasons.append("references no REQ-*")
            if bad_stage:
                reasons.append(f"stage {r['stage']!r} not in {{usable_early, releasable}}")
            offenders.append({"id": r["id"], "lineno": r["lineno"], "reasons": reasons})

    bar_testable = "PASS" if not offenders and not parse_problems else "FAIL"

    report = {
        "count_total": len(records),
        "stage_counts": dict(stage_counts),
        "area_counts": {a: dict(c) for a, c in area_counts.items()},
        "distinct_reqs_referenced": len(inv_sorted),
        "offenders": offenders,
        "parse_problems": parse_problems,
        "bar_testable": bar_testable,
        "records": records,
        "inversion": inv_sorted,
        "method_counts": {m: sum(1 for r in records if r["method"] == m) for m in sorted(VERIF_VOCAB)},
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
