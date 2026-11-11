#!/usr/bin/env python3
"""Independent re-verification of the operational-readiness synthesis gate.

Authored THIS invocation (reconstructed synthesis node). Re-derives every one of the
six contract identities directly from the on-disk artifacts — the assembled deliverable,
the five concern fragments, and the two upstream designs — WITHOUT trusting any prior
run's recorded verdicts. Also re-derives the quantitative claims the fold record states
and scans the deliverable for repository-hygiene violations.

Pure/read-only: reads files, prints evidence, exits 0 iff every identity PASSes.
"""
import re

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_operational_readiness"
DAG  = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1"
DELIV = BASE + "/SUBTASK_ops_synthesis/outputs/operational-readiness.md"

FRAGS = [
    ("durable_data",         BASE + "/SUBTASK_ops_durable_data/outputs/durable-data.md",        (1, 19)),
    ("backups_and_recovery", BASE + "/SUBTASK_ops_backups_recovery/outputs/backups-recovery.md",(20, 39)),
    ("limits_and_quotas",    BASE + "/SUBTASK_ops_limits_quotas/outputs/limits-quotas.md",      (40, 59)),
    ("observability",        BASE + "/SUBTASK_ops_observability/outputs/observability.md",      (60, 79)),
    ("status_and_incident",  BASE + "/SUBTASK_ops_status_incident/outputs/status-incident.md",  (80, 99)),
]
REQUIRED_SECTIONS = ["durable_data", "backups_and_recovery", "limits_and_quotas",
                     "observability", "status_and_incident",
                     "existing_followups", "requirements_and_acceptance_criteria"]
VMETHODS = {"manual_user_check", "automated_test", "inspection", "operational_check"}
FIELDS = ("statement", "acceptance_criteria", "verification_method", "release_gating", "traces_to")

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

REQ_HEAD = re.compile(r'^#### (REQ-OPS-\d{3}) ')

def extract_blocks(text):
    """verbatim (id, block_text) for each #### REQ-OPS block, up to the next #### or a
    narrative heading (# / ## / ###)."""
    lines = text.split("\n"); out = []; i = 0
    while i < len(lines):
        m = REQ_HEAD.match(lines[i])
        if not m:
            i += 1; continue
        rid = m.group(1); blk = [lines[i]]; i += 1
        while i < len(lines) and not lines[i].startswith("#### ") and not re.match(r'^#{1,3} (?!#)', lines[i]):
            blk.append(lines[i]); i += 1
        out.append((rid, "\n".join(blk).rstrip()))
    return out

def field(block, name):
    m = re.search(r'^- \*\*' + name + r'\*\*:\s*(.*)$', block, re.M)
    return m.group(1).strip() if m else None

results = []
def check(idn, ok, evidence):
    results.append((idn, bool(ok), evidence))
    return ok

# ---- collect fragment requirement blocks ----
frag_blocks = {}
all_frag = []
for sec, path, rng in FRAGS:
    b = extract_blocks(read(path))
    frag_blocks[sec] = (b, rng)
    all_frag.extend(b)
frag_ids = [r for r, _ in all_frag]

deliv = read(DELIV)

# ---- IDENTITY 1: ALL_SECTIONS_PRESENT (present + in order) ----
heads = re.findall(r'^## (\S+)\s*$', deliv, re.M)
check("ALL_SECTIONS_PRESENT", heads == REQUIRED_SECTIONS,
      f"deliverable ## headings = {heads}; required = {REQUIRED_SECTIONS}")

# ---- IDENTITY 2: CONCERN_COVERAGE (each concern >=1 req, all within its partition range) ----
cov_ok = True; cov_ev = []
for sec, path, rng in FRAGS:
    b, (lo, hi) = frag_blocks[sec]
    nums = [int(r.split('-')[-1]) for r, _ in b]
    inrange = all(lo <= n <= hi for n in nums)
    cov_ok = cov_ok and len(nums) > 0 and inrange
    cov_ev.append(f"{sec}={len(nums)} [{min(nums)}..{max(nums)}]⊂{lo}..{hi} ok={inrange}")
check("CONCERN_COVERAGE", cov_ok, " | ".join(cov_ev))

# ---- IDENTITY 3: NO_NUMBER_COLLISION (unique; register is verbatim union in id order) ----
dup = sorted({x for x in frag_ids if frag_ids.count(x) > 1})
reg_start = deliv.index("## requirements_and_acceptance_criteria")
reg_text = deliv[reg_start:]
reg_blocks = extract_blocks(reg_text)
reg_ids = [r for r, _ in reg_blocks]
reg_by_id = dict(reg_blocks)
verbatim_mismatch = [rid for rid, txt in all_frag if reg_by_id.get(rid) != txt]
sorted_ok = reg_ids == sorted(reg_ids)
union_equal = set(reg_ids) == set(frag_ids) and len(reg_ids) == len(frag_ids)
unique_ok = len(set(frag_ids)) == len(frag_ids)
check("NO_NUMBER_COLLISION",
      not dup and unique_ok and union_equal and sorted_ok and not verbatim_mismatch,
      f"frag_ids={len(frag_ids)} unique={len(set(frag_ids))} dups={dup or 'none'}; "
      f"register_ids={len(reg_ids)}; union_equal={union_equal}; sorted={sorted_ok}; "
      f"verbatim_mismatch={verbatim_mismatch or 'none'}")

# ---- IDENTITY 4: OPS_TESTABLE (vm in vocab; release_gating bool; gating => acceptance_criteria) ----
bad = []; vm_counts = {}; rg_true = 0; rg_false = 0
for rid, txt in all_frag:
    st = field(txt, "statement"); ac = field(txt, "acceptance_criteria")
    vm = field(txt, "verification_method"); rg = field(txt, "release_gating")
    vm_counts[vm] = vm_counts.get(vm, 0) + 1
    if rg == "true": rg_true += 1
    elif rg == "false": rg_false += 1
    problems = []
    if not st: problems.append("no_statement")
    if vm not in VMETHODS: problems.append(f"bad_vm({vm!r})")
    if rg not in ("true", "false"): problems.append(f"bad_gating({rg!r})")
    if rg == "true" and not (ac and ac.strip()): problems.append("gating_no_ac")
    if problems:
        bad.append(f"{rid}:{'/'.join(problems)}")
check("OPS_TESTABLE", not bad,
      f"n={len(all_frag)}; vm_counts={vm_counts}; release_gating true={rg_true} false={rg_false}; "
      f"problems={bad or 'none'}")

# ---- IDENTITY 5: OPS_TRACES (every traces_to target resolves in upstream designs) ----
prod = read(DAG + "/SUBTASK_product_requirements/outputs/product-requirements.md")
dom  = read(DAG + "/SUBTASK_domain_app_design/outputs/domain-application-design.md")
# "defined" = appears as a #### / ### heading id; fall back to any occurrence in source.
def defined(text, prefix):
    h = set(re.findall(r'^#{3,4} (' + prefix + r'-\d{3})', text, re.M))
    return h if h else set(re.findall(prefix + r'-\d{3}', text))
defined_prod = defined(prod, "REQ-PROD")
defined_dom  = defined(dom,  "REQ-DOM")
unresolved = []; no_trace = []
for rid, txt in all_frag:
    tr = field(txt, "traces_to") or ""
    tgts = re.findall(r'REQ-(?:PROD|DOM)-\d{3}', tr)
    if not tgts:
        no_trace.append(rid); continue
    for t in tgts:
        pool = defined_prod if t.startswith("REQ-PROD") else defined_dom
        if t not in pool:
            unresolved.append(f"{rid}->{t}")
check("OPS_TRACES", not unresolved,
      f"defined REQ-PROD={len(defined_prod)} REQ-DOM={len(defined_dom)}; "
      f"unresolved={unresolved or 'none'}; ops_internal(empty traces_to)={no_trace}")

# ---- IDENTITY 6: FOLLOWUPS_FOLDED (#23/#24/#25 each once in existing_followups; none minted) ----
fu_start = deliv.index("## existing_followups")
fu_end = deliv.index("## requirements_and_acceptance_criteria")
fu_text = deliv[fu_start:fu_end]
fold_rows = re.findall(r'^\|\s*(#2[345])\s*\|', fu_text, re.M)
one_row_each = sorted(fold_rows) == ["#23", "#24", "#25"]
# none minted as a new REQ-OPS: every union id is within the five concern ranges (001..099),
# and the follow-up section mints no new #### REQ-OPS block.
minted_beyond = [r for r in frag_ids if not (1 <= int(r.split('-')[-1]) <= 99)]
fu_minted = extract_blocks(fu_text)
check("FOLLOWUPS_FOLDED",
      one_row_each and not minted_beyond and not fu_minted,
      f"fold_rows={sorted(fold_rows)}; one_row_each={one_row_each}; "
      f"minted_beyond_ranges={minted_beyond or 'none'}; new_reqs_in_followups={[r for r,_ in fu_minted] or 'none'}")

# ---- HYGIENE scan (binding on repository-bound deliverable) ----
hygiene_patterns = {
    "ipv4_host":        r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    "ssh_key_path":     r'nousix_server_ed25519|\.ssh/',
    "abs_fs_path":      r'/home/\w+|/taskflow/|/nousix-runtime',
    "taskflow_id":      r'\bSUBTASK_|\bdesign-chirp-r1\b|\bproc-[0-9a-f]{8}',
    "attribution":      r'Co-Authored-By|Generated with \[Claude|🤖',
    "ssh_user_at":      r'mattm@',
}
hygiene_hits = {}
for name, pat in hygiene_patterns.items():
    hits = re.findall(pat, deliv)
    if hits:
        hygiene_hits[name] = sorted(set(hits))[:8]
check("HYGIENE", not hygiene_hits, f"violations={hygiene_hits or 'none'}")

# ---- quantitative summary (claims that appear in the fold record) ----
per_concern = {sec: len(frag_blocks[sec][0]) for sec, _, _ in FRAGS}
total = len(all_frag)
gating = rg_true
internal_ids = no_trace

print("=" * 74)
print("OPERATIONAL-READINESS SYNTHESIS GATE — INDEPENDENT IDENTITY RE-VERIFICATION")
print("=" * 74)
print(f"deliverable: {DELIV}")
print(f"  lines={len(deliv.splitlines())}  bytes={len(deliv)}")
print(f"requirements total={total}  release_gating={gating}  non_gating={total-gating}")
print(f"per-concern counts: {per_concern}")
print(f"defined upstream ids: REQ-PROD={len(defined_prod)}  REQ-DOM={len(defined_dom)}")
print(f"OPS-internal (empty traces_to): {internal_ids}")
print("-" * 74)
for idn, ok, ev in results:
    print(f"[{'PASS' if ok else 'FAIL'}] {idn}")
    print(f"       {ev}")
print("-" * 74)
allpass = all(ok for _, ok, _ in results)
print("ALL IDENTITIES: " + ("PASS" if allpass else "FAIL — reported, not plugged"))
import sys
sys.exit(0 if allpass else 1)
