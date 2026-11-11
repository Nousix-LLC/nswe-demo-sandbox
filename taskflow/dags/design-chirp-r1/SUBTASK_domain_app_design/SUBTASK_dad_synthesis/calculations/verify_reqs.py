#!/usr/bin/env python3
"""Synthesis-gate verification for SUBTASK_domain_app_design.
Reads the three part files; asserts REQ-DOM-* well-formedness, ranges, non-collision,
field presence, and that every traces_to target resolves to a real REQ-PROD-*."""
import re, sys

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_domain_app_design"
PARTS = {
    "SUBTASK_domain_model":      (f"{BASE}/SUBTASK_domain_model/outputs/domain-model.md",      (1, 49)),
    "SUBTASK_persistence_state": (f"{BASE}/SUBTASK_persistence_state/outputs/persistence-state.md", (100, 149)),
    "SUBTASK_module_structure":  (f"{BASE}/SUBTASK_module_structure/outputs/module-structure.md", (200, 249)),
}
PROD = f"{BASE}/SUBTASK_product_requirements/outputs/product-requirements.md"

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

# --- product requirement ids that exist (REQ-PROD-NNN) ---
prod_ids = set(int(n) for n in re.findall(r"REQ-PROD-(\d{3})", read(PROD)))
print(f"REQ-PROD ids present: {min(prod_ids):03d}..{max(prod_ids):03d}  count={len(prod_ids)}")

all_ids = []
problems = []
traces = {}   # req-dom id -> list of prod ints cited in its block

for owner, (path, (lo, hi)) in PARTS.items():
    text = read(path)
    # split into requirement blocks by the '#### REQ-DOM-NNN' heading
    blocks = re.split(r"(?m)^#### REQ-DOM-(\d{3})\b", text)
    # blocks[0] is preamble; then pairs (num, body)
    found = []
    for i in range(1, len(blocks), 2):
        num = int(blocks[i]); body = blocks[i+1]
        found.append(num)
        all_ids.append(num)
        # range check
        if not (lo <= num <= hi):
            problems.append(f"{owner}: REQ-DOM-{num:03d} outside declared range {lo}..{hi}")
        # field presence
        if "**statement**" not in body:
            problems.append(f"REQ-DOM-{num:03d}: missing statement")
        if "**acceptance_criteria**" not in body:
            problems.append(f"REQ-DOM-{num:03d}: missing acceptance_criteria")
        m = re.search(r"\*\*release_gating\*\*:\s*(true|false)", body)
        if not m:
            problems.append(f"REQ-DOM-{num:03d}: missing/!bool release_gating")
        # collect traces_to prod ids cited in the body (traces_to line only)
        tl = re.search(r"\*\*traces_to\*\*:\s*(.+)", body)
        cited = set(int(n) for n in re.findall(r"REQ-PROD-(\d{3})", tl.group(1))) if tl else set()
        traces[num] = cited
    print(f"{owner}: {len(found)} reqs -> {['%03d'%n for n in found]}")

# uniqueness / collision
dupes = sorted(n for n in set(all_ids) if all_ids.count(n) > 1)
print(f"\nTotal REQ-DOM count: {len(all_ids)}  unique: {len(set(all_ids))}")
if dupes:
    problems.append(f"DUPLICATE REQ-DOM ids: {dupes}")

# every traces_to target resolves
unresolved = {f"REQ-DOM-{d:03d}": sorted(c - prod_ids) for d, c in traces.items() if (c - prod_ids)}
if unresolved:
    problems.append(f"traces_to targets not in REQ-PROD set: {unresolved}")
n_traced = sum(1 for c in traces.values() if c)
print(f"REQ-DOM with >=1 REQ-PROD trace: {n_traced}; all cited targets resolve: {not unresolved}")

# release_gating tally
print()
for owner, (path, _) in PARTS.items():
    t = read(path)
    print(f"{owner}: release_gating true={len(re.findall(r'release_gating\*\*: true', t))} "
          f"false={len(re.findall(r'release_gating\*\*: false', t))}")

print("\n=== PROBLEMS ===")
if problems:
    for p in problems:
        print(" -", p)
    sys.exit(1)
print("none — all mechanical identities hold")
