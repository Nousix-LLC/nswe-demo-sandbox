#!/usr/bin/env python3
"""Mechanical union + verification for SUBTASK_journeys_fold.

Unions the nine journey-cluster verdict tables into one bar_id-keyed table over the
139 manual_user_check BAR-*, and asserts the sub-contract identities. Verbatim carry-
through: observations are copied exactly as each cluster wrote them; verdicts are never
re-judged. Any discrepancy is reported as a named gap, never silently reconciled.
"""
import re
import sys

HUB = ".."  # run from SUBTASK_journeys_fold/
RELEASE_BAR = "../../../../SUBTASK_release_bar/outputs/release-bar.md"
MANIFEST = "../contracts/_MANIFEST.yaml"
VOCAB = {"met", "partial", "missing", "not_applicable"}
METHODS = {"manual_user_check", "automated_test", "inspection", "operational_check"}

CLUSTER_FILES = {
    "SUBTASK_getin_identity":       "../SUBTASK_getin_identity/outputs/getin-identity-measurement.md",
    "SUBTASK_core_loop":            "../SUBTASK_core_loop/outputs/core-loop-measurement.md",
    "SUBTASK_account_lifecycle":    "../SUBTASK_account_lifecycle/outputs/account-lifecycle-measurement.md",
    "SUBTASK_resilience_states":    "../SUBTASK_resilience_states/outputs/resilience-states-measurement.md",
    "SUBTASK_safety_trust_support": "../SUBTASK_safety_trust_support/outputs/safety-trust-support-measurement.md",
    "SUBTASK_visual_craft_nav":     "../SUBTASK_visual_craft_nav/outputs/visual-craft-nav-measurement.md",
    "SUBTASK_responsive_phone":     "../SUBTASK_responsive_phone/outputs/responsive-phone-measurement.md",
    "SUBTASK_accessibility":        "../SUBTASK_accessibility/outputs/accessibility-measurement.md",
    "SUBTASK_web_delivery_api":     "../SUBTASK_web_delivery_api/outputs/web-delivery-api-measurement.md",
}

BAR_RE = re.compile(r"^BAR-\d{3}$")


def die(msg):
    print("FATAL:", msg)
    sys.exit(1)


def read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


# ---- 1. Authoritative sets from the release bar -------------------------------------
def parse_release_bar(text):
    """Return dict bar_id -> method for every criterion row, and the manual set."""
    by_method = {}
    # Criterion rows: **BAR-NNN** (`stage` · `method`) — ...
    row = re.compile(r"^\*\*(BAR-\d{3})\*\*\s*\(([^)]*)\)")
    for line in text.splitlines():
        m = row.match(line.strip())
        if not m:
            continue
        bar_id = m.group(1)
        toks = re.findall(r"`([^`]+)`", m.group(2))
        methods = [t for t in toks if t in METHODS]
        if len(methods) != 1:
            die(f"release bar {bar_id}: could not resolve a single method from {toks}")
        by_method[bar_id] = methods[0]
    return by_method


# ---- 2. Contract partition ----------------------------------------------------------
def parse_manifest(text):
    part_block = text.split("partition:", 1)[1].split("expected_counts:", 1)[0]
    partition = {}
    # split into per-cluster chunks
    chunks = re.split(r"\n\s*(SUBTASK_\w+):", part_block)
    # chunks[0] is preamble; then alternating name, body
    for i in range(1, len(chunks), 2):
        name = chunks[i]
        body = chunks[i + 1]
        bars = re.findall(r"BAR-\d{3}", body)
        partition[name] = bars
    ec_block = text.split("expected_counts:", 1)[1].split("ownership:", 1)[0]
    expected = {}
    for m in re.finditer(r"(SUBTASK_\w+|total):\s*(\d+)", ec_block):
        expected[m.group(1)] = int(m.group(2))
    return partition, expected


# ---- 3. Cluster verdict tables ------------------------------------------------------
def parse_cluster(path):
    rows = []
    for line in read(path).splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        s = s[1:]
        if s.endswith("|"):
            s = s[:-1]
        parts = s.split("|", 2)
        if len(parts) != 3:
            continue
        bar_id, status, obs = (p.strip() for p in parts)
        if not BAR_RE.match(bar_id):
            continue
        rows.append((bar_id, status, obs))
    return rows


def numkey(bar_id):
    return int(bar_id.split("-")[1])


def main():
    report = []
    gaps = []

    rb = parse_release_bar(read(RELEASE_BAR))
    manual_set = {b for b, m in rb.items() if m == "manual_user_check"}
    report.append(f"release bar: {len(rb)} criterion rows total; "
                  f"{len(manual_set)} with verification_method=manual_user_check")

    partition, expected = parse_manifest(read(MANIFEST))
    part_union = []
    for c, bars in partition.items():
        part_union.extend(bars)
    part_set = set(part_union)
    report.append(f"contract partition: {sum(len(v) for v in partition.values())} assignments "
                  f"across {len(partition)} clusters; {len(part_set)} distinct")

    # contract partition disjoint?
    if len(part_union) != len(part_set):
        seen, dup = set(), set()
        for b in part_union:
            if b in seen:
                dup.add(b)
            seen.add(b)
        gaps.append(f"CONTRACT partition not disjoint: duplicate assignment(s) {sorted(dup)}")

    # contract partition == release-bar manual set?
    if part_set != manual_set:
        miss = sorted(manual_set - part_set, key=numkey)
        extra = sorted(part_set - manual_set, key=numkey)
        if miss:
            gaps.append(f"CONTRACT partition missing manual_user_check BAR-*: {miss}")
        if extra:
            gaps.append(f"CONTRACT partition includes non-manual BAR-*: {extra}")

    # ---- union the nine cluster tables ----
    union = {}          # bar_id -> (status, obs)
    owner = {}          # bar_id -> cluster
    per_cluster_status = {}
    for cluster, path in CLUSTER_FILES.items():
        rows = parse_cluster(path)
        ids = [r[0] for r in rows]
        exp_ids = set(partition.get(cluster, []))
        got_ids = set(ids)

        # count vs expected_counts
        exp_n = expected.get(cluster)
        if exp_n is not None and len(ids) != exp_n:
            gaps.append(f"{cluster}: emitted {len(ids)} rows, expected_counts says {exp_n}")

        # intra-cluster duplicate
        if len(ids) != len(got_ids):
            d = sorted({b for b in ids if ids.count(b) > 1}, key=numkey)
            gaps.append(f"{cluster}: duplicate bar_id row(s) within cluster: {d}")

        # exact match to the contract's assignment for this cluster
        if got_ids != exp_ids:
            miss = sorted(exp_ids - got_ids, key=numkey)
            extra = sorted(got_ids - exp_ids, key=numkey)
            if miss:
                gaps.append(f"{cluster}: contract assigns but cluster did not judge: {miss}")
            if extra:
                gaps.append(f"{cluster}: cluster judged but contract did not assign: {extra}")

        sc = {"met": 0, "partial": 0, "missing": 0, "not_applicable": 0}
        for bar_id, status, obs in rows:
            if status not in VOCAB:
                gaps.append(f"{cluster}/{bar_id}: live_status '{status}' not in vocab")
            if not obs:
                gaps.append(f"{cluster}/{bar_id}: empty observation")
            if bar_id in union:
                gaps.append(f"CROSS-CLUSTER duplicate {bar_id}: in {owner[bar_id]} and {cluster}")
            else:
                union[bar_id] = (status, obs)
                owner[bar_id] = cluster
            if status in sc:
                sc[status] += 1
        per_cluster_status[cluster] = sc
        report.append(f"{cluster}: {len(ids)} rows  "
                      f"(met {sc['met']}, partial {sc['partial']}, missing {sc['missing']}, "
                      f"n/a {sc['not_applicable']})")

    union_set = set(union)

    # ---- totality: union == 139 == manual_set ----
    report.append(f"UNION: {len(union_set)} distinct bar_id")
    if union_set != manual_set:
        miss = sorted(manual_set - union_set, key=numkey)
        extra = sorted(union_set - manual_set, key=numkey)
        if miss:
            gaps.append(f"UNION missing manual_user_check BAR-* (in release bar, not measured): {miss}")
        if extra:
            gaps.append(f"UNION has BAR-* not manual_user_check in release bar: {extra}")

    total_expected = expected.get("total")
    if total_expected is not None and len(union_set) != total_expected:
        gaps.append(f"UNION size {len(union_set)} != contract total {total_expected}")

    # vocab/format final sweep
    for bar_id, (status, obs) in union.items():
        if not BAR_RE.match(bar_id):
            gaps.append(f"malformed bar_id {bar_id}")
        if status not in VOCAB:
            gaps.append(f"{bar_id}: status '{status}' not in vocab")

    # ---- totals ----
    totals = {"met": 0, "partial": 0, "missing": 0, "not_applicable": 0}
    for status, _ in union.values():
        if status in totals:
            totals[status] += 1

    print("=== VERIFICATION REPORT ===")
    for r in report:
        print(" ", r)
    print()
    print("=== IDENTITY ASSERTIONS ===")
    assertions = [
        ("CLUSTER_DISJOINT_TOTAL", not any(g.startswith(("CROSS-CLUSTER", "UNION", "CONTRACT")) or
                                           "contract assigns" in g or "contract did not assign" in g or
                                           "expected_counts" in g or "duplicate" in g for g in gaps)),
        ("MANUAL_STATUS_TOTAL", all(st in VOCAB for st, _ in union.values()) and
                                len(union) == (total_expected or len(union)) and
                                all(o for _, o in union.values())),
        ("VOCAB_CONFORMS", all(st in VOCAB for st, _ in union.values()) and
                           all(BAR_RE.match(b) for b in union)),
    ]
    for name, ok in assertions:
        print(f"  {name}: {'PASS' if ok else 'FAIL'}")
    print()
    print("=== TOTALS (union of 139) ===")
    print(f"  met {totals['met']}, partial {totals['partial']}, "
          f"missing {totals['missing']}, not_applicable {totals['not_applicable']}, "
          f"TOTAL {sum(totals.values())}")
    print()
    if gaps:
        print("=== GAPS (named, NOT reconciled) ===")
        for g in gaps:
            print("  -", g)
    else:
        print("=== GAPS: NONE — partition disjoint & total, vocab conforms, observations grounded ===")

    # ---- write the union table rows for the fold to assemble ----
    ordered = sorted(union.items(), key=lambda kv: numkey(kv[0]))
    with open("union_table.md", "w", encoding="utf-8") as f:
        f.write("| bar_id | live_status | observation |\n")
        f.write("|--------|-------------|-------------|\n")
        for bar_id, (status, obs) in ordered:
            f.write(f"| {bar_id} | {status} | {obs} |\n")

    # machine summary line for SYNTHESIS
    pcs = "; ".join(f"{c.replace('SUBTASK_','')}={expected.get(c)}" for c in CLUSTER_FILES)
    print()
    print("=== PER-CLUSTER EXPECTED COUNTS ===")
    print(" ", pcs, "; total=", total_expected)
    print("WROTE union_table.md with", len(ordered), "rows")


if __name__ == "__main__":
    main()
