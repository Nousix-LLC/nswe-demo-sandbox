#!/usr/bin/env python3
"""Independent verification of the operational-readiness synthesis gate (reconstructed node).
Re-derives every contract identity from the five fragments + the assembled deliverable,
rather than trusting the prior invocation's recorded verdicts."""
import re, sys

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_operational_readiness"
DAG  = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1"
DELIV = BASE + "/SUBTASK_ops_synthesis/outputs/operational-readiness.md"

FRAGS = [
    ("durable_data",        BASE + "/SUBTASK_ops_durable_data/outputs/durable-data.md",   (1, 19)),
    ("backups_and_recovery",BASE + "/SUBTASK_ops_backups_recovery/outputs/backups-recovery.md",(20,39)),
    ("limits_and_quotas",   BASE + "/SUBTASK_ops_limits_quotas/outputs/limits-quotas.md", (40,59)),
    ("observability",       BASE + "/SUBTASK_ops_observability/outputs/observability.md", (60,79)),
    ("status_and_incident", BASE + "/SUBTASK_ops_status_incident/outputs/status-incident.md",(80,99)),
]
REQUIRED_SECTIONS = ["durable_data","backups_and_recovery","limits_and_quotas","observability",
                     "status_and_incident","existing_followups","requirements_and_acceptance_criteria"]
VMETHODS = {"manual_user_check","automated_test","inspection","operational_check"}

def read(p):
    with open(p, encoding="utf-8") as f: return f.read()

REQ_HEAD = re.compile(r'^#### (REQ-OPS-\d{3}) ')
def extract_blocks(text):
    """verbatim (id, block_text) for each #### REQ-OPS block up to next #### or narrative #/##/### heading."""
    lines = text.split("\n"); out=[]; i=0
    while i < len(lines):
        m = REQ_HEAD.match(lines[i])
        if not m: i+=1; continue
        rid=m.group(1); blk=[lines[i]]; i+=1
        while i < len(lines) and not lines[i].startswith("#### ") and not re.match(r'^#{1,3} (?!#)', lines[i]):
            blk.append(lines[i]); i+=1
        out.append((rid, "\n".join(blk).rstrip()))
    return out

def field(block, name):
    m = re.search(r'\*\*'+name+r'\*\*:\s*(.*)', block)
    return m.group(1).strip() if m else None

results = []
def check(idn, ok, evidence):
    results.append((idn, "PASS" if ok else "FAIL", evidence)); return ok

# ---- collect fragment blocks ----
frag_blocks = {}   # section -> list[(id, text)]
all_frag = []      # (id, text) in fragment order
for sec, path, (lo,hi) in FRAGS:
    b = extract_blocks(read(path))
    frag_blocks[sec] = b
    all_frag.extend(b)

deliv = read(DELIV)

# ---- ALL_SECTIONS_PRESENT ----
heads = re.findall(r'^## (\S+)', deliv, re.M)
check("ALL_SECTIONS_PRESENT", heads == REQUIRED_SECTIONS,
      f"deliverable ## headings = {heads}; required order = {REQUIRED_SECTIONS}")

# ---- CONCERN_COVERAGE + range ----
cov_ok=True; cov_ev=[]
for sec, path, (lo,hi) in FRAGS:
    ids=[int(r.split('-')[-1]) for r,_ in frag_blocks[sec]]
    inrange = all(lo<=n<=hi for n in ids)
    cov_ev.append(f"{sec}: {len(ids)} reqs, range_ok={inrange} ({min(ids)}..{max(ids)} vs {lo}..{hi})")
    cov_ok = cov_ok and len(ids)>0 and inrange
check("CONCERN_COVERAGE", cov_ok, " | ".join(cov_ev))

# ---- NO_NUMBER_COLLISION + verbatim union ----
frag_ids=[r for r,_ in all_frag]
dup = [x for x in frag_ids if frag_ids.count(x)>1]
# register blocks = blocks under requirements_and_acceptance_criteria section
reg_start = deliv.index("## requirements_and_acceptance_criteria")
reg_text = deliv[reg_start:]
reg_blocks = extract_blocks(reg_text)
reg_ids = [r for r,_ in reg_blocks]
# verbatim match: each fragment block text appears byte-for-byte in register (by id)
frag_by_id = dict(all_frag); reg_by_id = dict(reg_blocks)
mismatch=[]
for rid, txt in all_frag:
    if reg_by_id.get(rid) != txt:
        mismatch.append(rid)
sorted_ok = reg_ids == sorted(reg_ids)
union_ok = (set(reg_ids)==set(frag_ids)) and len(reg_ids)==len(frag_ids) and not mismatch
check("NO_NUMBER_COLLISION",
      not dup and union_ok and sorted_ok and len(set(frag_ids))==len(frag_ids),
      f"{len(frag_ids)} frag ids, {len(reg_ids)} register ids, dup_frag={dup}, "
      f"verbatim_mismatch={mismatch}, register_sorted={sorted_ok}, union_equal={set(reg_ids)==set(frag_ids)}")

# ---- OPS_TESTABLE ----
test_ok=True; bad=[]
for rid, txt in all_frag:
    st=field(txt,"statement"); ac=field(txt,"acceptance_criteria")
    vm=field(txt,"verification_method"); rg=field(txt,"release_gating")
    vm_ok = vm in VMETHODS
    rg_ok = rg in ("true","false")
    gating = rg=="true"
    ac_ok = (ac is not None and len(ac)>0) if gating else True
    if not (st and vm_ok and rg_ok and ac_ok):
        bad.append(f"{rid}(st={bool(st)},vm={vm},rg={rg},ac={bool(ac)})")
    test_ok = test_ok and st and vm_ok and rg_ok and ac_ok
vm_counts={}; rg_true=rg_false=0
for rid,txt in all_frag:
    vm_counts[field(txt,"verification_method")]=vm_counts.get(field(txt,"verification_method"),0)+1
    if field(txt,"release_gating")=="true": rg_true+=1
    else: rg_false+=1
check("OPS_TESTABLE", test_ok,
      f"bad={bad or 'none'}; vm_counts={vm_counts}; release_gating true={rg_true} false={rg_false}; n={len(all_frag)}")

# ---- OPS_TRACES ----
prod = read(DAG + "/SUBTASK_product_requirements/outputs/product-requirements.md")
dom  = read(DAG + "/SUBTASK_domain_app_design/outputs/domain-application-design.md")
defined_prod=set(re.findall(r'REQ-PROD-\d{3}', " ".join(re.findall(r'^#### (REQ-PROD-\d{3})', prod, re.M))))
defined_dom =set(re.findall(r'REQ-DOM-\d{3}',  " ".join(re.findall(r'^#### (REQ-DOM-\d{3})',  dom,  re.M))))
# fall back: any heading style
if not defined_prod: defined_prod=set(re.findall(r'REQ-PROD-\d{3}', prod))
if not defined_dom:  defined_dom =set(re.findall(r'REQ-DOM-\d{3}',  dom))
trace_ok=True; unresolved=[]; no_trace=[]
for rid, txt in all_frag:
    tr=field(txt,"traces_to")
    tgts=re.findall(r'REQ-(?:PROD|DOM)-\d{3}', tr or "")
    if not tgts: no_trace.append(rid); continue
    for t in tgts:
        pool = defined_prod if t.startswith("REQ-PROD") else defined_dom
        if t not in pool: unresolved.append(f"{rid}->{t}"); trace_ok=False
check("OPS_TRACES", trace_ok,
      f"defined PROD={len(defined_prod)} DOM={len(defined_dom)}; unresolved={unresolved or 'none'}; "
      f"ops-internal(no-trace)={no_trace}")

# ---- FOLLOWUPS_FOLDED ----
fu_start = deliv.index("## existing_followups")
fu_text = deliv[fu_start:deliv.index("## requirements_and_acceptance_criteria")]
fu_ok=True; fu_ev=[]
for num in ("#23","#24","#25"):
    present = num in fu_text
    fu_ev.append(f"{num} in existing_followups={present}")
    fu_ok = fu_ok and present
# ensure not minted as new REQ: ids are all within 5 concern ranges only (already checked); count stays 75
minted_beyond = [r for r in frag_ids if not (1<=int(r.split('-')[-1])<=99)]
check("FOLLOWUPS_FOLDED", fu_ok and not minted_beyond,
      " | ".join(fu_ev)+f"; no new minted REQ beyond ranges={not minted_beyond}")

print("="*70)
for idn,verdict,ev in results:
    print(f"[{verdict}] {idn}\n      {ev}")
print("="*70)
allpass = all(v=="PASS" for _,v,_ in results)
print("ALL IDENTITIES PASS" if allpass else "SOME IDENTITIES FAILED")
sys.exit(0 if allpass else 1)
