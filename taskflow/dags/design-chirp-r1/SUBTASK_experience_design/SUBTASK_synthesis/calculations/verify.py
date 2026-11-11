import re, os

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_experience_design"
PROD = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_product_requirements/outputs/product-requirements.md"

# owner -> (file, lo, hi)
SOURCES = [
    ("ia_interaction",     "SUBTASK_ia_interaction/outputs/ia-interaction.md",                                   1, 19),
    ("visual_system",      "SUBTASK_visual_system/outputs/visual-system.md",                                     20, 39),
    ("get_in",             "SUBTASK_screens_flows/SUBTASK_get_in/outputs/screens-get-in.md",                     40, 50),
    ("core_loop",          "SUBTASK_screens_flows/SUBTASK_core_loop/outputs/screens-core-loop.md",               51, 64),
    ("account_lifecycle",  "SUBTASK_screens_flows/SUBTASK_account_lifecycle/outputs/screens-account-lifecycle.md",65, 77),
    ("safety_notifications","SUBTASK_screens_flows/SUBTASK_safety_notifications/outputs/screens-safety-notifications.md",78,85),
    ("considered_states",  "SUBTASK_screens_flows/SUBTASK_considered_states/outputs/empty-error-loading-states.md",86,89),
    ("responsive",         "SUBTASK_responsive/outputs/responsive.md",                                           90, 99),
    ("accessibility",      "SUBTASK_accessibility/outputs/accessibility.md",                                     100,119),
]

HEAD = re.compile(r'^#{2,6}\s+REQ-UX-(\d{3})\b', re.M)
PROD_REF = re.compile(r'REQ-PROD-(\d{3})')

def blocks(text):
    """Yield (num, body) for each REQ-UX heading block up to the next heading of same/shallower level."""
    heads = [(m.start(), int(m.group(1))) for m in HEAD.finditer(text)]
    out = []
    for i,(pos,num) in enumerate(heads):
        end = heads[i+1][0] if i+1 < len(heads) else len(text)
        out.append((num, text[pos:end]))
    return out

defined = {}   # num -> list of (owner, has_stmt, has_ac, gating, prodrefs)
dup = []
for owner, rel, lo, hi in SOURCES:
    path = os.path.join(BASE, rel)
    text = open(path, encoding="utf-8").read()
    seen_here = {}
    for num, body in blocks(text):
        # dedupe repeated headings inside one file (none expected) - keep richest
        has_stmt = ("**statement**" in body)
        has_ac   = ("**acceptance_criteria**" in body)
        mg = re.search(r'\*\*release_gating\*\*\s*:\s*(true|false)', body)
        gating = mg.group(1) if mg else None
        mref = re.search(r'\*\*references\*\*\s*:\s*(.+)', body)
        if mref:
            refs = sorted(set("REQ-PROD-%03d"%int(x) for x in PROD_REF.findall(mref.group(1))))
        else:
            refs = sorted(set("REQ-PROD-%03d"%int(x) for x in PROD_REF.findall(body)))
        rec = (owner, has_stmt, has_ac, gating, refs, lo, hi)
        if num in seen_here:
            # merge: prefer the block that has statement/refs
            prev = seen_here[num]
            if (has_stmt or refs) and not (prev[1] or prev[4]):
                seen_here[num] = rec
            continue
        seen_here[num] = rec
    for num, rec in seen_here.items():
        defined.setdefault(num, []).append(rec)

# ---- ID_UNIQUE_IN_RANGE
collisions = {n:recs for n,recs in defined.items() if len(recs)>1}
out_of_range = []
for n, recs in defined.items():
    for rec in recs:
        owner, _,_,_,_, lo, hi = rec
        if not (lo <= n <= hi):
            out_of_range.append((n, owner, lo, hi))

expected = set(range(1,120))
present = set(defined.keys())
missing = sorted(expected - present)
extra   = sorted(present - expected)

# ---- UX_TESTABLE_AND_GATED + each has >=1 prod ref
no_stmt=[]; no_ac=[]; no_gate=[]; no_ref=[]
ux_to_prod = {}
for n, recs in defined.items():
    rec = recs[0]
    owner, has_stmt, has_ac, gating, refs, lo, hi = rec
    if not has_stmt: no_stmt.append(n)
    if not has_ac: no_ac.append(n)
    if gating is None: no_gate.append(n)
    if not refs: no_ref.append(n)
    ux_to_prod["REQ-UX-%03d"%n] = refs

# ---- parse REQ-PROD register
ptext = open(PROD, encoding="utf-8").read()
phead = re.compile(r'^#{2,6}\s+REQ-PROD-(\d{3})\b.*$', re.M)
prod = {}
pmatches = [(m.start(), int(m.group(1)), m.group(0)) for m in phead.finditer(ptext)]
for i,(pos,num,title) in enumerate(pmatches):
    end = pmatches[i+1][0] if i+1 < len(pmatches) else len(ptext)
    body = ptext[pos:end]
    mg = re.search(r'\*\*release_gating\*\*\s*:\s*(true|false)', body)
    prod[num] = {"gating": mg.group(1) if mg else None, "title": title.strip("# ").strip()}

prod_ids = sorted(prod.keys())

# reverse coverage: which REQ-PROD referenced by >=1 REQ-UX
covered = set()
for refs in ux_to_prod.values():
    for r in refs:
        covered.add(int(r.split("-")[-1]))

# contract's UX-surface set that MUST be covered or recorded-with-reason
must = set(range(30,37))                        # experience-quality 030-036
must |= (set(range(1,29)) | {32,33,34,42})      # user-facing surface of 001-028, 032-034, 042
must &= set(prod_ids)
uncovered_must = sorted(must - covered)

print("="*70)
print("REQ-UX CONSOLIDATED REGISTER — VERIFICATION")
print("="*70)
print("Total REQ-UX defined:", len(defined), "(expected 119)")
print("Missing ids:", missing)
print("Extra/out-of-expected ids:", extra)
print()
print("--- ID_UNIQUE_IN_RANGE ---")
print("Collisions (id defined in >1 owner file):", {n:[r[0] for r in recs] for n,recs in collisions.items()} or "NONE")
print("Out-of-range ids:", out_of_range or "NONE")
print()
print("--- UX_TESTABLE_AND_GATED ---")
print("Missing statement:", no_stmt or "NONE")
print("Missing acceptance_criteria:", no_ac or "NONE")
print("Missing release_gating flag:", no_gate or "NONE")
print()
print("--- UX_TRACES_TO_PROD (forward: each REQ-UX -> >=1 REQ-PROD) ---")
print("REQ-UX with NO REQ-PROD reference:", no_ref or "NONE")
# referenced prod ids that don't exist
bad_refs = {}
for ux, refs in ux_to_prod.items():
    for r in refs:
        if int(r.split("-")[-1]) not in prod:
            bad_refs.setdefault(ux,[]).append(r)
print("REQ-UX referencing a non-existent REQ-PROD:", bad_refs or "NONE")
print()
print("--- UX_TRACES_TO_PROD (reverse: REQ-PROD UX-surface coverage) ---")
print("REQ-PROD total in register:", len(prod_ids), "range", min(prod_ids), "-", max(prod_ids))
print("REQ-PROD covered by >=1 REQ-UX:", len(covered))
print("Contract 'must-cover' UX-surface set size:", len(must))
print("Uncovered among must-cover set:", uncovered_must or "NONE")
print()
print("All REQ-PROD NOT referenced by any REQ-UX (for the record):")
print(sorted(set(prod_ids)-covered))
print()
# gating summary
gate_counts = {"true":0,"false":0,None:0}
for recs in defined.values():
    gate_counts[recs[0][3]] = gate_counts.get(recs[0][3],0)+1
print("--- release_gating distribution ---", gate_counts)
print()
print("--- per-owner id counts ---")
from collections import Counter
cnt = Counter(recs[0][0] for recs in defined.values())
for owner,_,lo,hi in SOURCES:
    ids = sorted(n for n,recs in defined.items() if recs[0][0]==owner)
    print(f"{owner:22s} range {lo:3d}-{hi:3d}  count={len(ids):2d}  min={min(ids) if ids else '-'} max={max(ids) if ids else '-'}")
print()
print("Full REQ-UX -> REQ-PROD trace table:")
for n in sorted(defined.keys()):
    print(f"  REQ-UX-{n:03d}  gating={defined[n][0][3]:5}  -> {', '.join(ux_to_prod['REQ-UX-%03d'%n])}")
