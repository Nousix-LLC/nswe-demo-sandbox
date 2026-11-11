#!/usr/bin/env python3
"""
Independent operational-readiness synthesis-gate verifier (re-derived this invocation).

Pure, read-only. Re-derives each of the six contract identities in
../contracts/_MANIFEST.yaml directly from the on-disk artifacts:
  - the five concern fragments (the source of truth for the requirements),
  - the assembled deliverable operational-readiness.md,
  - the two upstream designs (for traceability-target resolution).
Exit 0 iff every identity PASSES and the hygiene scan is clean; non-zero otherwise.
Trusts no prior run's verdict.
"""
import re, sys, os

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1"
OPS  = f"{BASE}/SUBTASK_operational_readiness"

FRAGMENTS = {
    "durable_data":        (f"{OPS}/SUBTASK_ops_durable_data/outputs/durable-data.md",      (1, 19)),
    "backups_and_recovery":(f"{OPS}/SUBTASK_ops_backups_recovery/outputs/backups-recovery.md",(20, 39)),
    "limits_and_quotas":   (f"{OPS}/SUBTASK_ops_limits_quotas/outputs/limits-quotas.md",     (40, 59)),
    "observability":       (f"{OPS}/SUBTASK_ops_observability/outputs/observability.md",      (60, 79)),
    "status_and_incident": (f"{OPS}/SUBTASK_ops_status_incident/outputs/status-incident.md",  (80, 99)),
}
DELIVERABLE = f"{OPS}/SUBTASK_ops_synthesis/outputs/operational-readiness.md"
PROD = f"{BASE}/SUBTASK_product_requirements/outputs/product-requirements.md"
DOM  = f"{BASE}/SUBTASK_domain_app_design/outputs/domain-application-design.md"

REQUIRED_SECTIONS = [
    "durable_data", "backups_and_recovery", "limits_and_quotas",
    "observability", "status_and_incident", "existing_followups",
    "requirements_and_acceptance_criteria",
]
VMETHODS = {"manual_user_check", "automated_test", "inspection", "operational_check"}
FIELDS = ("statement", "acceptance_criteria", "verification_method", "release_gating", "traces_to")

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def parse_reqs(text, header_re):
    """Parse REQ-OPS blocks. header_re captures the id on a heading line.
    Returns ordered list of (id, {field: value})."""
    lines = text.splitlines()
    out = []
    cur_id = None
    cur = {}
    def flush():
        if cur_id is not None:
            out.append((cur_id, dict(cur)))
    for ln in lines:
        m = header_re.match(ln)
        if m:
            flush()
            cur_id = m.group(1)
            cur = {}
            continue
        if cur_id is not None:
            fm = re.match(r'^- \*\*(statement|acceptance_criteria|verification_method|release_gating|traces_to)\*\*:\s*(.*)$', ln)
            if fm:
                cur[fm.group(1)] = fm.group(2).strip()
            elif re.match(r'^#{1,6}\s', ln):
                # a new heading that is not a req header closes the current block
                flush(); cur_id = None; cur = {}
    flush()
    return out

def idnum(reqid):
    return int(reqid.rsplit("-", 1)[1])

results = []   # (identity, verdict_bool, evidence)
def record(idn, ok, ev):
    results.append((idn, ok, ev))

# ---- Parse fragments (source of truth) --------------------------------------
frag_header = re.compile(r'^#### (REQ-OPS-\d{3})\b')
frag_reqs = {}          # id -> fields
frag_by_section = {}    # section -> [ids]
collisions = []
range_violations = []
for sec, (path, (lo, hi)) in FRAGMENTS.items():
    reqs = parse_reqs(read(path), frag_header)
    ids = []
    for rid, fields in reqs:
        ids.append(rid)
        if rid in frag_reqs:
            collisions.append(rid)
        frag_reqs[rid] = fields
        n = idnum(rid)
        if not (lo <= n <= hi):
            range_violations.append((rid, sec, lo, hi))
    frag_by_section[sec] = ids

# ---- Parse deliverable ------------------------------------------------------
dtext = read(DELIVERABLE)
sec_headers = [m.group(1).strip() for m in re.finditer(r'^## (.+)$', dtext, re.M)]
# section bodies carry reqs at ##### ; register carries them at ####
body_reqs = parse_reqs(dtext, re.compile(r'^##### (REQ-OPS-\d{3})\b'))
reg_reqs  = parse_reqs(dtext, re.compile(r'^#### (REQ-OPS-\d{3})\b'))

# ---- Identity 1: ALL_SECTIONS_PRESENT ---------------------------------------
ok1 = sec_headers == REQUIRED_SECTIONS
record("ALL_SECTIONS_PRESENT", ok1,
       f"deliverable ## keys = {sec_headers}; required = {REQUIRED_SECTIONS}; equal={ok1}")

# ---- Identity 2: CONCERN_COVERAGE -------------------------------------------
cov_detail = {}
ok2 = True
for sec, (_, (lo, hi)) in FRAGMENTS.items():
    ids = frag_by_section[sec]
    in_range = all(lo <= idnum(i) <= hi for i in ids)
    cov_detail[sec] = (len(ids), f"{min(idnum(i) for i in ids):03d}..{max(idnum(i) for i in ids):03d}", f"{lo:03d}..{hi:03d}")
    if not ids or not in_range:
        ok2 = False
# also every concern body present in deliverable with its reqs
body_ids = {rid for rid, _ in body_reqs}
for sec in FRAGMENTS:
    for rid in frag_by_section[sec]:
        if rid not in body_ids:
            ok2 = False
record("CONCERN_COVERAGE", ok2,
       "; ".join(f"{s}: {c[0]} reqs {c[1]} in {c[2]}" for s, c in cov_detail.items())
       + f"; all fragment ids present in section bodies={all(r in body_ids for r in frag_reqs)}")

# ---- Identity 3: NO_NUMBER_COLLISION + verbatim union -----------------------
all_ids = list(frag_reqs.keys())
unique_ok = len(all_ids) == len(set(all_ids)) and not collisions
range_ok = not range_violations
reg_ids = [rid for rid, _ in reg_reqs]
reg_unique_ok = len(reg_ids) == len(set(reg_ids))
# register set equals fragment set
set_match = set(reg_ids) == set(frag_reqs.keys())
# register sorted in id order
sorted_ok = reg_ids == sorted(reg_ids, key=idnum)
# verbatim: every field of every register block equals the fragment block
field_mismatches = []
for rid, rf in reg_reqs:
    ff = frag_reqs.get(rid, {})
    for k in FIELDS:
        if rf.get(k, "<MISSING>") != ff.get(k, "<MISSING>"):
            field_mismatches.append((rid, k))
ok3 = unique_ok and range_ok and reg_unique_ok and set_match and sorted_ok and not field_mismatches
record("NO_NUMBER_COLLISION", ok3,
       f"{len(all_ids)} fragment ids, {len(set(all_ids))} unique, collisions={collisions or 'none'}, "
       f"range_violations={range_violations or 'none'}; register {len(reg_ids)} ids, set==fragments={set_match}, "
       f"sorted={sorted_ok}, verbatim_field_mismatches={field_mismatches or 'none'}")

# ---- Identity 4: OPS_TESTABLE -----------------------------------------------
vm_counts = {}
rg_counts = {True: 0, False: 0}
test_problems = []
for rid, f in frag_reqs.items():
    vm = f.get("verification_method", "")
    vm_counts[vm] = vm_counts.get(vm, 0) + 1
    if vm not in VMETHODS:
        test_problems.append((rid, f"bad vm {vm!r}"))
    rg_raw = f.get("release_gating", "").lower()
    if rg_raw not in ("true", "false"):
        test_problems.append((rid, f"bad release_gating {rg_raw!r}"))
    gating = rg_raw == "true"
    rg_counts[gating] = rg_counts.get(gating, 0) + 1
    if not f.get("statement"):
        test_problems.append((rid, "empty statement"))
    if gating and not f.get("acceptance_criteria"):
        test_problems.append((rid, "gating but empty acceptance_criteria"))
ok4 = not test_problems
record("OPS_TESTABLE", ok4,
       f"vm={vm_counts}; release_gating true={rg_counts[True]} false={rg_counts[False]}; problems={test_problems or 'none'}")

# ---- Identity 5: OPS_TRACES -------------------------------------------------
def defined_ids(path, area):
    return set(re.findall(rf'^#{{2,5}} (REQ-{area}-\d+)\b', read(path), re.M))
prod_ids = defined_ids(PROD, "PROD")
dom_ids = defined_ids(DOM, "DOM")
defined = prod_ids | dom_ids
unresolved = []
empty_traces = []
for rid, f in frag_reqs.items():
    raw = f.get("traces_to", "").strip()
    if raw == "" or raw == "—":
        empty_traces.append(rid)
        continue
    for tgt in [t.strip() for t in raw.split(",") if t.strip()]:
        tgt = tgt.strip("`")
        if tgt not in defined:
            unresolved.append((rid, tgt))
ok5 = not unresolved
record("OPS_TRACES", ok5,
       f"{len(prod_ids)} REQ-PROD + {len(dom_ids)} REQ-DOM defined upstream; "
       f"unresolved={unresolved or 'none'}; empty traces_to (permitted, OPS-internal)={sorted(empty_traces)}")

# ---- Identity 6: FOLLOWUPS_FOLDED -------------------------------------------
fu_section = dtext.split("## existing_followups", 1)[1].split("## requirements_and_acceptance_criteria", 1)[0] if "## existing_followups" in dtext else ""
fu_ok = True
fu_detail = []
for issue in ("#23", "#24", "#25"):
    n = len(re.findall(rf'\|\s*{re.escape(issue)}\s*\|', fu_section))
    gating_near = re.findall(rf'\|\s*{re.escape(issue)}\s*\|.*\|\s*(No|Yes)\s*\|', fu_section)
    placed = n == 1
    nongating = gating_near == ["No"]
    fu_detail.append(f"{issue}: rows={n}, gating_col={gating_near}")
    if not (placed and nongating):
        fu_ok = False
# no new REQ-OPS minted in the followups section
minted = re.findall(r'^#{3,5} (REQ-OPS-\d+)', fu_section, re.M)
if minted:
    fu_ok = False
# all register ids lie within the five concern ranges (nothing minted outside)
range_lo, range_hi = 1, 99
outside = [i for i in reg_ids if not (range_lo <= idnum(i) <= range_hi)]
if outside:
    fu_ok = False
record("FOLLOWUPS_FOLDED", fu_ok,
       "; ".join(fu_detail) + f"; new REQ-OPS minted in followups={minted or 'none'}")

# ---- Hygiene scan on the deliverable ----------------------------------------
hy = []
if re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', dtext):
    hy.append("IPv4 address")
if re.search(r'/home/\w+', dtext):
    hy.append("absolute home path")
if re.search(r'\.ssh/|_ed25519|BatchMode', dtext):
    hy.append("ssh key material")
if re.search(r'taskflow/|SUBTASK_|_GLOBAL\.md|_BRIEF\.md|proc-[0-9a-f]', dtext):
    hy.append("taskflow/agent/dag identifier")
if re.search(r'Co-Authored-By|Generated with|claude\.com/claude-code', dtext):
    hy.append("attribution footer")
if re.search(r'k3d|k3s|kubectl|argocd', dtext, re.I):
    hy.append("cluster tooling name")
hy_ok = not hy
record("HYGIENE", hy_ok, f"flags={hy or 'clean'}")

# ---- Report -----------------------------------------------------------------
print(f"Fragments parsed: {len(frag_reqs)} REQ-OPS requirements")
print(f"Register blocks:  {len(reg_reqs)}")
print(f"Section-body blocks: {len(body_reqs)}")
print("-" * 72)
all_ok = True
for idn, ok, ev in results:
    print(f"[{'PASS' if ok else 'FAIL'}] {idn}")
    print(f"       {ev}")
    all_ok = all_ok and ok
print("-" * 72)
print("ALL PASS" if all_ok else "FAILURES PRESENT")
sys.exit(0 if all_ok else 1)
