import re, os, json

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_experience_design"
PROD = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_product_requirements/outputs/product-requirements.md"

# owner -> (assembled file, lo, hi)  — the CONTRACT-correct five assembled sibling outputs
SOURCES = [
    ("ia_interaction", "SUBTASK_ia_interaction/outputs/ia-interaction.md",   1,  19),
    ("visual_system",  "SUBTASK_visual_system/outputs/visual-system.md",    20,  39),
    ("screens_flows",  "SUBTASK_screens_flows/outputs/screens-flows.md",    40,  89),
    ("responsive",     "SUBTASK_responsive/outputs/responsive.md",          90,  99),
    ("accessibility",  "SUBTASK_accessibility/outputs/accessibility.md",   100, 119),
]

HEAD = re.compile(r'^#{2,6}\s+REQ-UX-(\d{3})\b', re.M)

def blocks(text):
    heads = [(m.start(), int(m.group(1))) for m in HEAD.finditer(text)]
    out = []
    for i, (pos, num) in enumerate(heads):
        end = heads[i+1][0] if i+1 < len(heads) else len(text)
        out.append((num, text[pos:end]))
    return out

defined = {}            # num -> list of records (owner, has_stmt, has_ac, gating, refs, lo, hi)
dup_here = []           # (num, owner) repeated headings within one file
for owner, rel, lo, hi in SOURCES:
    text = open(os.path.join(BASE, rel), encoding="utf-8").read()
    seen_here = {}
    for num, body in blocks(text):
        has_stmt = bool(re.search(r'\*\*statement\*\*\s*:', body))
        has_ac   = bool(re.search(r'\*\*acceptance_criteria\*\*\s*:', body))
        mg = re.search(r'\*\*release_gating\*\*\s*:\s*(true|false)', body)
        gating = mg.group(1) if mg else None
        # forward trace: REQ-PROD ids on the **references** line only
        mref = re.search(r'\*\*references\*\*\s*:\s*(.+)', body)
        refs = sorted(set("REQ-PROD-%03d" % int(x) for x in re.findall(r'REQ-PROD-(\d{3})', mref.group(1)))) if mref else []
        rec = (owner, has_stmt, has_ac, gating, refs, lo, hi)
        if num not in seen_here:
            seen_here[num] = rec
        else:
            dup_here.append((num, owner))
    for num, rec in seen_here.items():
        defined.setdefault(num, []).append(rec)

# ---- ID_UNIQUE_IN_RANGE
collisions = {n: [r[0] for r in recs] for n, recs in defined.items() if len(recs) > 1}
out_of_range = []
for n, recs in defined.items():
    for rec in recs:
        owner, _, _, _, _, lo, hi = rec
        if not (lo <= n <= hi):
            out_of_range.append((n, owner, lo, hi))

expected = set(range(1, 120))
present = set(defined.keys())
missing = sorted(expected - present)
extra = sorted(present - expected)

# ---- UX_TESTABLE_AND_GATED + forward trace
no_stmt = []; no_ac = []; no_gate = []; no_ref = []
ux_to_prod = {}
for n, recs in defined.items():
    owner, has_stmt, has_ac, gating, refs, lo, hi = recs[0]
    if not has_stmt: no_stmt.append(n)
    if not has_ac: no_ac.append(n)
    if gating is None: no_gate.append(n)
    if not refs: no_ref.append(n)
    ux_to_prod["REQ-UX-%03d" % n] = refs

# ---- REQ-PROD register
ptext = open(PROD, encoding="utf-8").read()
phead = re.compile(r'^#{2,6}\s+REQ-PROD-(\d{3})\b.*$', re.M)
pm = [(m.start(), int(m.group(1)), m.group(0)) for m in phead.finditer(ptext)]
prod = {}
for i, (pos, num, title) in enumerate(pm):
    end = pm[i+1][0] if i+1 < len(pm) else len(ptext)
    body = ptext[pos:end]
    mg = re.search(r'\*\*release_gating\*\*\s*:\s*(true|false)', body)
    prod[num] = {"gating": mg.group(1) if mg else None}
prod_ids = sorted(prod.keys())

covered = set()
for refs in ux_to_prod.values():
    for r in refs:
        covered.add(int(r.split("-")[-1]))

bad_refs = {ux: [r for r in refs if int(r.split("-")[-1]) not in prod] for ux, refs in ux_to_prod.items() if any(int(r.split("-")[-1]) not in prod for r in refs)}

# contract must-cover UX-surface set: experience-quality 030-036 + user-facing surface of 001-028, 032-034, 042
must = set(range(30, 37)) | set(range(1, 29)) | {32, 33, 34, 42}
must &= set(prod_ids)
uncovered_must = sorted(must - covered)

print("="*72)
print("REQ-UX CONSOLIDATED REGISTER — GATE VERIFICATION (against assembled outputs)")
print("="*72)
print("Total REQ-UX defined:", len(defined), "(expected 119)")
print("Missing ids:", missing or "NONE")
print("Extra/out-of-expected ids:", extra or "NONE")
print()
print("--- ID_UNIQUE_IN_RANGE ---")
print("Collisions:", collisions or "NONE")
print("Out-of-range ids:", out_of_range or "NONE")
print()
print("--- UX_TESTABLE_AND_GATED ---")
print("Missing statement:", no_stmt or "NONE")
print("Missing acceptance_criteria:", no_ac or "NONE")
print("Missing release_gating flag:", no_gate or "NONE")
print()
print("--- UX_TRACES_TO_PROD (forward) ---")
print("REQ-UX with NO REQ-PROD reference:", no_ref or "NONE")
print("REQ-UX referencing a non-existent REQ-PROD:", bad_refs or "NONE")
print()
print("--- UX_TRACES_TO_PROD (reverse: must-cover UX surfaces) ---")
print("REQ-PROD register size:", len(prod_ids), "range", min(prod_ids), "-", max(prod_ids))
print("Distinct REQ-PROD covered by >=1 REQ-UX:", len(covered))
print("Must-cover UX-surface set size:", len(must))
print("Uncovered among must-cover set:", uncovered_must or "NONE")
print("All REQ-PROD NOT referenced by any REQ-UX (for record):", sorted(set(prod_ids) - covered))
print()
gc = {"true": 0, "false": 0, None: 0}
for recs in defined.values():
    gc[recs[0][3]] = gc.get(recs[0][3], 0) + 1
print("--- release_gating distribution (REQ-UX) ---", gc)
print()
print("--- per-owner id counts ---")
for owner, rel, lo, hi in SOURCES:
    ids = sorted(n for n, recs in defined.items() if recs[0][0] == owner)
    print(f"{owner:16s} range {lo:3d}-{hi:3d}  count={len(ids):2d}  min={min(ids) if ids else '-'} max={max(ids) if ids else '-'}")
print()
print("REQ-PROD gating map:", json.dumps({f"{k:03d}": prod[k]['gating'] for k in prod_ids}))
