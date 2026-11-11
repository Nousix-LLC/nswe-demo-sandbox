#!/usr/bin/env python3
"""Verification-gate checker for SUBTASK_dad_synthesis.
Reads the consolidated design file, the three part outputs, and the product-requirements
register (paths passed as argv). Emits recorded evidence for the contract identities.
Pure read + report; writes nothing.
"""
import re
import sys

consolidated, p_model, p_persist, p_module, p_prod = sys.argv[1:6]

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

RANGES = {
    "domain_model": range(1, 50),        # 001..049
    "persistence_state": range(100, 150),  # 100..149
    "module_structure": range(200, 250),   # 200..249
}

req_hdr = re.compile(r'^####\s+(REQ-DOM-(\d{3}))\s+[—-]\s+(.+)$', re.M)

def parse_reqs(text):
    """Return list of (id, num, title, body) for each REQ-DOM block in text."""
    blocks = []
    matches = list(req_hdr.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(text)
        body = text[start:end]
        blocks.append((m.group(1), int(m.group(2)), m.group(3).strip(), body))
    return blocks

cons = read(consolidated)
cons_reqs = parse_reqs(cons)

# ---- Identity 2: REQ_DOM_WELL_FORMED ----
field_pat = {
    "statement": re.compile(r'-\s*\*\*statement\*\*\s*:', re.I),
    "acceptance_criteria": re.compile(r'-\s*\*\*acceptance_criteria\*\*\s*:', re.I),
    "release_gating": re.compile(r'-\s*\*\*release_gating\*\*\s*:\s*(true|false)\b', re.I),
}
malformed = []
gating_true = gating_false = 0
for rid, num, title, body in cons_reqs:
    miss = [k for k in ("statement", "acceptance_criteria") if not field_pat[k].search(body)]
    g = field_pat["release_gating"].search(body)
    if not g:
        miss.append("release_gating")
    else:
        if g.group(1).lower() == "true":
            gating_true += 1
        else:
            gating_false += 1
    if miss:
        malformed.append((rid, miss))

# ---- Identity 3: REQ_DOM_NO_COLLISION + ranges ----
ids = [r[0] for r in cons_reqs]
nums = [r[1] for r in cons_reqs]
dupes = sorted({x for x in ids if ids.count(x) > 1})
in_some_range = lambda n: any(n in rg for rg in RANGES.values())
out_of_range = [r[0] for r in cons_reqs if not in_some_range(r[1])]

# ---- Union check vs the three parts ----
def ids_in(path):
    return {m[0] for m in parse_reqs(read(path))}
model_ids = ids_in(p_model)
persist_ids = ids_in(p_persist)
module_ids = ids_in(p_module)
parts_union = model_ids | persist_ids | module_ids
cons_id_set = set(ids)
missing_from_cons = sorted(parts_union - cons_id_set)
extra_in_cons = sorted(cons_id_set - parts_union)

# range membership per part source
def band_violations(id_set, rg, label):
    bad = [i for i in id_set if int(i.split('-')[-1]) not in rg]
    return bad
model_band = band_violations(model_ids, RANGES["domain_model"], "model")
persist_band = band_violations(persist_ids, RANGES["persistence_state"], "persist")
module_band = band_violations(module_ids, RANGES["module_structure"], "module")

# ---- Identity 6: REQ_DOM_TRACES_PROD ----
prod_defined = set(re.findall(r'REQ-PROD-\d{3}', read(p_prod)))
traces_pat = re.compile(r'-\s*\*\*traces_to\*\*\s*:\s*(.+)')
cited = set()
reqs_with_traces = 0
for rid, num, title, body in cons_reqs:
    tt = traces_pat.search(body)
    if tt:
        found = re.findall(r'REQ-PROD-\d{3}', tt.group(1))
        if found:
            reqs_with_traces += 1
            cited.update(found)
unresolved = sorted(cited - prod_defined)

# ---- Identity 7: REPO_HYGIENE (leakage scan) ----
hygiene_terms = [
    r'SUBTASK_', r'_GLOBAL', r'_BRIEF', r'SYNTHESIS\.md', r'COMPLETE\.md',
    r'taskflow', r'decompose', r'NeedsDecompose', r'100\.90\.75\.93',
    r'nousix_server_ed25519', r'k3d', r'kubectl', r'Co-Authored-By',
    r'Generated with', r'claude', r'proc-[0-9a-f]{8}',
]
hygiene_hits = {}
for t in hygiene_terms:
    found = re.findall(t, cons, re.I)
    if found:
        hygiene_hits[t] = len(found)
# HTML authoring comments
html_comments = re.findall(r'<!--.*?-->', cons, re.S)

print("== REQ register ==")
print(f"total REQ-DOM blocks in consolidated: {len(cons_reqs)}")
print(f"unique ids: {len(cons_id_set)}  duplicates: {dupes or 'none'}")
print(f"out-of-range ids: {out_of_range or 'none'}")
print(f"release_gating: true={gating_true} false={gating_false} (sum={gating_true+gating_false})")
print(f"gating=false ids: {[r[0] for r in cons_reqs if field_pat['release_gating'].search(r[3]) and field_pat['release_gating'].search(r[3]).group(1).lower()=='false']}")
print()
print("== well-formed ==")
print(f"malformed blocks (missing fields): {malformed or 'none'}")
print()
print("== union vs parts ==")
print(f"model ids={len(model_ids)} persist ids={len(persist_ids)} module ids={len(module_ids)} parts_union={len(parts_union)}")
print(f"in parts but missing from consolidated: {missing_from_cons or 'none'}")
print(f"in consolidated but not in any part (newly minted?): {extra_in_cons or 'none'}")
print(f"band violations: model={model_band or 'none'} persist={persist_band or 'none'} module={module_band or 'none'}")
print()
print("== traces ==")
print(f"REQ-DOM with traces_to: {reqs_with_traces}")
print(f"distinct REQ-PROD cited: {len(cited)}  unresolved (cited but undefined): {unresolved or 'none'}")
print(f"cited set sample: {sorted(cited)[:50]}")
print()
print("== hygiene ==")
print(f"forbidden-term hits: {hygiene_hits or 'none'}")
print(f"HTML authoring comments: {len(html_comments)}")
# sorted id listing for the record
print()
print("== all consolidated ids (sorted) ==")
print(','.join(sorted(cons_id_set)))
