"""
Diagnostics for SKELETON_COMPLETE: break down the release-gating REQ-* that carry bar_ids
but no direct backlog (epic, issue) trace, grouped by area, so the finding is surfaced exactly.

Part of: SUBTASK_assemble (identity-traceability synthesis gate), design-chirp-r1.
Depends on: calc_001 (same inputs; re-parsed here so this script is independently runnable).
"""
import re

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_synthesis/SUBTASK_identity_traceability"
SKELETONS = [f"{BASE}/SUBTASK_matrix_prod_dom/outputs/skeleton-prod-dom.md",
             f"{BASE}/SUBTASK_matrix_ux/outputs/skeleton-ux.md",
             f"{BASE}/SUBTASK_matrix_id_ops/outputs/skeleton-id-ops.md"]
BAR_MAP = f"{BASE}/SUBTASK_bar_mapping/outputs/bar-mapping.md"
BACKLOG = f"{BASE}/SUBTASK_backlog_pr/outputs/backlog-pr.md"

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()
def numkey(r):
    m = re.match(r"REQ-([A-Z]+)-(\d+)", r); return (m.group(1), int(m.group(2)))

gating = {}
rr = re.compile(r"^\|\s*(REQ-[A-Z]+-\d+)\s*\|\s*(true|false)\s*\|")
for p in SKELETONS:
    for ln in read(p).splitlines():
        m = rr.match(ln.strip())
        if m: gating[m.group(1)] = (m.group(2) == "true")

bar_ids = {}
sec2 = read(BAR_MAP).split("## 2. Inverted")[1].split("\n---")[0]
for ln in sec2.splitlines():
    m = re.match(r"^\|\s*(REQ-[A-Z]+-\d+)\s*\|\s*([^|]+?)\s*\|\s*$", ln.strip())
    if m:
        bar_ids[m.group(1)] = [b.strip() for b in m.group(2).split(",") if b.strip().startswith("BAR-")]

issues = {}
a2 = read(BACKLOG).split("### A.2")[1].split("### A.3")[0]
for ln in a2.splitlines():
    m = re.match(r"^\|\s*(REQ-[A-Z]+-\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$", ln.strip())
    if m:
        issues[m.group(1)] = [x.strip() for x in m.group(3).split(",") if x.strip().startswith("#")]

gating_reqs = sorted([r for r in gating if gating[r]], key=numkey)
no_issue = [r for r in gating_reqs if bar_ids.get(r) and not issues.get(r)]

by_area = {}
for r in no_issue:
    a = r.split("-")[1]
    by_area.setdefault(a, []).append(r)

print(f"gating reqs with bar_ids but NO direct backlog issue trace: {len(no_issue)}")
for a in sorted(by_area):
    lst = by_area[a]
    print(f"\n{a} ({len(lst)}):")
    print("  " + ", ".join(lst))

# also: gating reqs WITH an issue trace, per area, for the covered tally
with_issue = [r for r in gating_reqs if issues.get(r)]
print(f"\ngating reqs WITH a direct backlog issue trace: {len(with_issue)} / {len(gating_reqs)}")
