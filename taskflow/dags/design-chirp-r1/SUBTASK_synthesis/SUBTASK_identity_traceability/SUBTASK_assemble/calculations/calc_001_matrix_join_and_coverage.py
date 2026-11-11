"""
Assemble the whole-DAG traceability-matrix skeleton and assert BAR_COVERS_GATING_REQS.

Part of: SUBTASK_assemble (identity-traceability synthesis gate), design-chirp-r1.
Depends on: None (self-contained; reads the six COMPLETED, read-only spoke outputs by absolute path).

Mechanical join per the sub-contract join_rule:
  one matrix row per REQ-*; req_id/release_gating from the owning design spoke (verbatim);
  design_doc_ref derived canonically as `design/<file>.md § <req_id>` from the inherited
  design_artifact_map area->file mapping; bar_ids from SUBTASK_bar_mapping's REQ->bar_ids;
  epic/issue_numbers from SUBTASK_backlog_pr's REQ->(epic,issue); live_status left empty.

Then the cross-source BAR_COVERS_GATING_REQS: every release-gating REQ-* has >=1 BAR-*.
No value is guessed or plugged; shortfalls are reported.
"""
import re

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_synthesis/SUBTASK_identity_traceability"
SK_PROD_DOM = f"{BASE}/SUBTASK_matrix_prod_dom/outputs/skeleton-prod-dom.md"
SK_UX       = f"{BASE}/SUBTASK_matrix_ux/outputs/skeleton-ux.md"
SK_ID_OPS   = f"{BASE}/SUBTASK_matrix_id_ops/outputs/skeleton-id-ops.md"
BAR_MAP     = f"{BASE}/SUBTASK_bar_mapping/outputs/bar-mapping.md"
BACKLOG     = f"{BASE}/SUBTASK_backlog_pr/outputs/backlog-pr.md"

AREA_FILE = {
    "PROD": "design/product-requirements.md",
    "DOM":  "design/domain-application-design.md",
    "UX":   "design/experience-design.md",
    "ID":   "design/identity-security.md",
    "OPS":  "design/operational-readiness.md",
}

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def area_of(req):
    # REQ-<AREA>-NNN
    return req.split("-")[1]

def numkey(req):
    m = re.match(r"REQ-([A-Z]+)-(\d+)", req)
    return (m.group(1), int(m.group(2)))

# ---- 1. Parse design-side skeleton rows: req_id -> release_gating (bool) ----
# Row shape in all three skeletons: | REQ-<AREA>-NNN | true|false | <design_doc_ref...> |
gating = {}            # req_id -> bool
gating_dups = []
row_re = re.compile(r"^\|\s*(REQ-[A-Z]+-\d+)\s*\|\s*(true|false)\s*\|")
for path in (SK_PROD_DOM, SK_UX, SK_ID_OPS):
    for line in read(path).splitlines():
        m = row_re.match(line.strip())
        if m:
            rid, g = m.group(1), (m.group(2) == "true")
            if rid in gating:
                gating_dups.append(rid)
            gating[rid] = g

# ---- 2. Parse REQ -> bar_ids from bar-mapping section 2 ----
bar_ids = {}           # req_id -> [BAR-*]
txt = read(BAR_MAP)
sec2 = txt.split("## 2. Inverted")[1]
sec2 = sec2.split("\n---")[0]
brow = re.compile(r"^\|\s*(REQ-[A-Z]+-\d+)\s*\|\s*([^|]+?)\s*\|\s*$")
for line in sec2.splitlines():
    m = brow.match(line.strip())
    if m:
        rid = m.group(1)
        bars = [b.strip() for b in m.group(2).split(",") if b.strip().startswith("BAR-")]
        bar_ids[rid] = bars

# ---- 3. Parse REQ -> (epics, issues) from backlog A.2 ----
epics = {}             # req_id -> [#epic]
issues = {}            # req_id -> [#issue]
bt = read(BACKLOG)
a2 = bt.split("### A.2")[1].split("### A.3")[0]
erow = re.compile(r"^\|\s*(REQ-[A-Z]+-\d+)\s*\|\s*([^|]+?)\s*\|\s*([^|]+?)\s*\|\s*$")
for line in a2.splitlines():
    m = erow.match(line.strip())
    if m:
        rid = m.group(1)
        ep = [x.strip() for x in m.group(2).split(",") if x.strip().startswith("#")]
        iss = [x.strip() for x in m.group(3).split(",") if x.strip().startswith("#")]
        epics[rid] = ep
        issues[rid] = iss

all_reqs = sorted(gating.keys(), key=numkey)
gating_reqs = [r for r in all_reqs if gating[r]]
nongating_reqs = [r for r in all_reqs if not gating[r]]

# ---- 4. BAR_COVERS_GATING_REQS: every release-gating REQ-* has >=1 BAR-* ----
gating_no_bar = [r for r in gating_reqs if not bar_ids.get(r)]

# ---- 5. Diagnostics ----
# per-area counts
areas = {}
for r in all_reqs:
    a = area_of(r)
    areas.setdefault(a, [0,0])
    areas[a][0] += 1
    if gating[r]:
        areas[a][1] += 1

# gating reqs with bar coverage but no direct backlog issue trace
gating_bar_no_issue = [r for r in gating_reqs if bar_ids.get(r) and not issues.get(r)]
# gating reqs with neither bar nor issue
gating_no_bar_no_issue = [r for r in gating_reqs if not bar_ids.get(r) and not issues.get(r)]

print("=== INPUT INTEGRITY ===")
print(f"design-side requirement rows parsed: {len(all_reqs)}")
print(f"  per area (total, gating): " + ", ".join(f"{a}=({t},{g})" for a,(t,g) in sorted(areas.items())))
print(f"duplicate req_id across skeletons: {sorted(set(gating_dups)) or 'none'}")
print(f"REQ->bar_ids keys parsed: {len(bar_ids)}")
print(f"REQ->(epic,issue) keys parsed: {len(epics)}")
print(f"total gating reqs: {len(gating_reqs)}  non-gating: {len(nongating_reqs)}")
print()
print("=== BAR_COVERS_GATING_REQS ===")
print(f"gating reqs covered by >=1 BAR-*: {len(gating_reqs)-len(gating_no_bar)}/{len(gating_reqs)}")
print(f"gating reqs with NO BAR-*: {len(gating_no_bar)}")
print(f"  list: {gating_no_bar or 'none'}")
print(f"VERDICT: {'PASS' if not gating_no_bar else 'FAIL'}")
print()
print("=== BACKLOG-TRACE DIAGNOSTICS (not part of BAR_COVERS_GATING_REQS) ===")
print(f"gating reqs with bar coverage but no direct backlog issue trace: {len(gating_bar_no_issue)}")
print(f"gating reqs with neither bar nor issue: {len(gating_no_bar_no_issue)}")
# sanity: bar_ids keys that are not in the req set (would indicate a bar enforcing an undefined req)
orphan_bar_keys = [r for r in bar_ids if r not in gating]
print(f"REQ->bar_ids keys not present in any design skeleton: {sorted(orphan_bar_keys, key=numkey) or 'none'}")
orphan_issue_keys = [r for r in epics if r not in gating]
print(f"REQ->(epic,issue) keys not present in any design skeleton: {sorted(orphan_issue_keys, key=numkey) or 'none'}")

# ---- 6. Emit the matrix markdown table ----
def cell_bars(r):
    b = bar_ids.get(r, [])
    return ", ".join(b) if b else ""
def cell_epics(r):
    e = epics.get(r, [])
    return ", ".join(e) if e else ""
def cell_issues(r):
    i = issues.get(r, [])
    return ", ".join(i) if i else ""

lines = []
lines.append("| req_id | release_gating | bar_ids | epic | issue_numbers | design_doc_ref | live_status |")
lines.append("|--------|----------------|---------|------|---------------|----------------|-------------|")
for r in all_reqs:
    a = area_of(r)
    ddr = f"`{AREA_FILE[a]}` § {r}"
    lines.append(f"| {r} | {str(gating[r]).lower()} | {cell_bars(r)} | {cell_epics(r)} | {cell_issues(r)} | {ddr} |  |")
out = "\n".join(lines) + "\n"
with open(f"{BASE}/SUBTASK_assemble/calculations/matrix_rows.md", "w", encoding="utf-8") as f:
    f.write(out)
print()
print(f"=== MATRIX EMITTED: {len(all_reqs)} rows to calculations/matrix_rows.md ===")
