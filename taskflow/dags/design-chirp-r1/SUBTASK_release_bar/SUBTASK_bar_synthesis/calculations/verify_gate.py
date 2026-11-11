#!/usr/bin/env python3
"""
Independent release-bar gate verification (SUBTASK_bar_synthesis).
Parses the five BAR fragments, the five area design docs, and the assembled
release-bar.md from scratch and checks each of the eight subtree identities.
Prints an auditable per-identity verdict. No dependency on prior tooling.
"""
import re, sys, json

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1"
RB = BASE + "/SUBTASK_release_bar"

VOCAB = {"manual_user_check", "automated_test", "inspection", "operational_check"}
STAGES = {"usable_early", "releasable"}

AREAS = {
    "PROD": {"frag": RB + "/SUBTASK_bar_prod/outputs/bar-prod.md",
             "design": BASE + "/SUBTASK_product_requirements/outputs/product-requirements.md",
             "lo": 1, "hi": 99},
    "DOM":  {"frag": RB + "/SUBTASK_bar_dom/outputs/bar-dom.md",
             "design": BASE + "/SUBTASK_domain_app_design/outputs/domain-application-design.md",
             "lo": 100, "hi": 199},
    "UX":   {"frag": RB + "/SUBTASK_bar_ux/outputs/bar-ux.md",
             "design": BASE + "/SUBTASK_experience_design/outputs/experience-design.md",
             "lo": 200, "hi": 299},
    "ID":   {"frag": RB + "/SUBTASK_bar_id/outputs/bar-id.md",
             "design": BASE + "/SUBTASK_identity_trust/outputs/identity-security.md",
             "lo": 300, "hi": 399},
    "OPS":  {"frag": RB + "/SUBTASK_bar_ops/outputs/bar-ops.md",
             "design": BASE + "/SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md",
             "lo": 400, "hi": 499},
}
DELIV = RB + "/outputs/release-bar.md"

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

REQ_RE = re.compile(r"REQ-[A-Z]+-\d{3}")

def parse_fragment(path):
    """Return dict bar_id -> {refs:set, method:str|None, stage:str|None, line:int}."""
    bars = {}
    lines = read(path).splitlines()
    cur = None
    for i, ln in enumerate(lines, 1):
        m = re.match(r"^#{2,4}\s+(BAR-\d{3})\b", ln.strip())
        if m:
            cur = m.group(1)
            bars[cur] = {"refs": set(), "method": None, "stage": None, "line": i}
            continue
        if ln.startswith("#"):          # any other heading ends the block
            cur = None
            continue
        if cur is None:
            continue
        low = ln.lower()
        if "**references**" in low:
            bars[cur]["refs"].update(REQ_RE.findall(ln))
        elif "**verification_method**" in low:
            v = ln.split(":", 1)[1].strip().strip("`").lower() if ":" in ln else ""
            bars[cur]["method"] = v
        elif "**proposed_stage**" in low:
            v = ln.split(":", 1)[1].strip().strip("`").lower() if ":" in ln else ""
            bars[cur]["stage"] = v
    return bars

def parse_gating(path, prefix):
    """Return (gating_set, info). A REQ block = '#### REQ-<prefix>-NNN' up to next
    heading of level 1-4. gating=True if block's release_gating is true. Dedup by id."""
    lines = read(path).splitlines()
    head_re = re.compile(r"^(#{1,4})\s+(REQ-%s-\d{3})\b" % prefix)
    any_head_re = re.compile(r"^#{1,4}\s")
    per_block = []   # (id, gating_bool_or_None)
    i = 0
    n = len(lines)
    while i < n:
        m = head_re.match(lines[i])
        if not m:
            i += 1
            continue
        rid = m.group(2)
        j = i + 1
        gating = None
        while j < n and not any_head_re.match(lines[j]):
            low = lines[j].lower()
            if "release_gating" in low and gating is None:
                if re.search(r"release_gating\*?\*?\s*:\s*`?true", low):
                    gating = True
                elif re.search(r"release_gating\*?\*?\s*:\s*`?false", low):
                    gating = False
            j += 1
        per_block.append((rid, gating))
        i = j
    # dedup: id is gating if ANY block marks it true; track conflicts / missing
    status = {}
    conflicts = []
    missing_flag = []
    for rid, g in per_block:
        if g is None:
            missing_flag.append(rid)
            g = False
        if rid in status and status[rid] != g:
            conflicts.append(rid)
            status[rid] = status[rid] or g
        else:
            status[rid] = status.get(rid, False) or g
    gating_set = {r for r, g in status.items() if g}
    info = {"distinct_reqs": len(status), "blocks": len(per_block),
            "gating": len(gating_set), "nongating": len(status) - len(gating_set),
            "conflicts": sorted(set(conflicts)), "missing_flag": sorted(set(missing_flag))}
    return gating_set, info

def parse_register(path):
    """Return dict bar_id -> {stage, method, refs:set, line}."""
    reg = {}
    bar_re = re.compile(r"\*\*(BAR-\d{3})\*\*\s*\(`([^`]+)`\s*[·‧\-]\s*`([^`]+)`\)")
    for i, ln in enumerate(read(path).splitlines(), 1):
        m = bar_re.search(ln)
        if not m:
            continue
        bid, stage, method = m.group(1), m.group(2).strip().lower(), m.group(3).strip().lower()
        refs = set()
        em = re.search(r"_Enforces ([^_]+?)\._", ln)
        if em:
            refs = set(REQ_RE.findall(em.group(1)))
        reg[bid] = {"stage": stage, "method": method, "refs": refs, "line": i}
    return reg

# ---------------- load everything ----------------
frag_bars = {}       # area -> {bar: {...}}
all_frag = {}        # bar -> {..., area}
dup_across = []
for area, cfg in AREAS.items():
    fb = parse_fragment(cfg["frag"])
    frag_bars[area] = fb
    for b, d in fb.items():
        if b in all_frag:
            dup_across.append(b)
        all_frag[b] = dict(d, area=area)

gating = {}
gating_info = {}
for area, cfg in AREAS.items():
    gs, info = parse_gating(cfg["design"], area)
    gating[area] = gs
    gating_info[area] = info

reg = parse_register(DELIV)
deliv_text = read(DELIV)

results = {}

# 1. BAR_RANGE_RESPECTED
oor = []
for area, cfg in AREAS.items():
    for b in frag_bars[area]:
        num = int(b.split("-")[1])
        if not (cfg["lo"] <= num <= cfg["hi"]):
            oor.append((area, b))
results["BAR_RANGE_RESPECTED"] = (not oor, {"out_of_range": oor,
    "per_area_counts": {a: len(frag_bars[a]) for a in AREAS}})

# 2. NO_BAR_COLLISION
results["NO_BAR_COLLISION"] = (not dup_across, {"total_bars": len(all_frag),
    "duplicates": sorted(set(dup_across))})

# 3. GATING_REQ_COVERAGE  (covered = referenced by >=1 BAR anywhere)
covered = set()
for b, d in all_frag.items():
    covered |= d["refs"]
uncovered = {}
for area in AREAS:
    miss = sorted(r for r in gating[area] if r not in covered)
    if miss:
        uncovered[area] = miss
results["GATING_REQ_COVERAGE"] = (not uncovered, {
    "gating_per_area": {a: gating_info[a]["gating"] for a in AREAS},
    "gating_total": sum(gating_info[a]["gating"] for a in AREAS),
    "parse_info": gating_info,
    "uncovered": uncovered})

# 4. BAR_TESTABLE
bad_method = []
no_ref = []
for b, d in all_frag.items():
    if d["method"] not in VOCAB:
        bad_method.append((b, d["method"]))
    if not d["refs"]:
        no_ref.append(b)
results["BAR_TESTABLE"] = (not bad_method and not no_ref,
    {"bad_method": bad_method, "no_reference": no_ref})

# 5. BAR_STAGED (uses the register's FINAL stages; register must cover exactly the fragment bars)
reg_ids = set(reg)
frag_ids = set(all_frag)
missing_from_reg = sorted(frag_ids - reg_ids)
extra_in_reg = sorted(reg_ids - frag_ids)
bad_stage = [(b, reg[b]["stage"]) for b in reg if reg[b]["stage"] not in STAGES]
# refs + method preserved verbatim fragment->register
ref_mismatch = []
method_mismatch = []
for b in sorted(frag_ids & reg_ids):
    if all_frag[b]["refs"] != reg[b]["refs"]:
        ref_mismatch.append((b, sorted(all_frag[b]["refs"]), sorted(reg[b]["refs"])))
    if all_frag[b]["method"] != reg[b]["method"]:
        method_mismatch.append((b, all_frag[b]["method"], reg[b]["method"]))
# per-area final stage counts from register
area_stage = {a: {"usable_early": 0, "releasable": 0} for a in AREAS}
def area_of(b):
    n = int(b.split("-")[1])
    for a, c in AREAS.items():
        if c["lo"] <= n <= c["hi"]:
            return a
    return None
for b in reg:
    a = area_of(b); s = reg[b]["stage"]
    if a and s in STAGES:
        area_stage[a][s] += 1
# parse the scoping "by area" table to compare
table_counts = {}
for ln in deliv_text.splitlines():
    m = re.match(r"\|\s*(.+?)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*$", ln)
    if m:
        table_counts[m.group(1).strip().strip("*").strip()] = (int(m.group(2)), int(m.group(3)), int(m.group(4)))
name2area = {"Product": "PROD", "Domain & application": "DOM", "Experience": "UX",
             "Identity, security & trust": "ID", "Operational readiness": "OPS"}
table_mismatch = []
for name, a in name2area.items():
    if name in table_counts:
        ue, rel, tot = table_counts[name]
        if (ue, rel) != (area_stage[a]["usable_early"], area_stage[a]["releasable"]):
            table_mismatch.append((name, (ue, rel), (area_stage[a]["usable_early"], area_stage[a]["releasable"])))
    else:
        table_mismatch.append((name, "MISSING_ROW", None))
staged_ok = (not missing_from_reg and not extra_in_reg and not bad_stage
             and not ref_mismatch and not method_mismatch and not table_mismatch)
results["BAR_STAGED"] = (staged_ok, {
    "missing_from_register": missing_from_reg, "extra_in_register": extra_in_reg,
    "bad_stage": bad_stage, "ref_mismatch": ref_mismatch[:20], "ref_mismatch_n": len(ref_mismatch),
    "method_mismatch": method_mismatch[:20], "method_mismatch_n": len(method_mismatch),
    "register_stage_counts_by_area": area_stage,
    "scoping_table_counts": table_counts, "table_mismatch": table_mismatch,
    "register_total": len(reg),
    "overall": {"usable_early": sum(area_stage[a]["usable_early"] for a in AREAS),
                "releasable": sum(area_stage[a]["releasable"] for a in AREAS)}})

# 6. SURFACE_GAP_RECORDED (mechanical presence check; prose judged separately by the agent)
gap_start = deliv_text.find("## Completeness and gap review")
gap = deliv_text[gap_start:] if gap_start >= 0 else ""
surfaces = ["sign-up", "sign-in", "recover", "account deletion", "data export",
            "onboarding", "settings", "notification", "admin", "support", "billing"]
surf_hits = {s: (s.lower() in gap.lower()) for s in surfaces}
results["SURFACE_GAP_RECORDED"] = (all(surf_hits.values()) and gap_start >= 0,
    {"section_present": gap_start >= 0, "surface_keyword_present": surf_hits,
     "section_len": len(gap)})

# 7. THREE_SECTIONS_PRESENT
h2 = [ln.strip() for ln in deliv_text.splitlines() if ln.startswith("## ")]
want = ["## MVP-vs-releasable scoping", "## Release bar", "## Completeness and gap review"]
results["THREE_SECTIONS_PRESENT"] = (h2 == want, {"found": h2, "expected": want})

# 8. HYGIENE (forbidden host/system/taskflow/attribution detail)
forbidden = {
    "ipv4": re.compile(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b"),
    "home_path": re.compile(r"/home/\w+"),
    "taskflow_path": re.compile(r"taskflow/|/dags/|nousix-runtime"),
    "subtask": re.compile(r"SUBTASK_"),
    "internal_record": re.compile(r"SYNTHESIS\.md|SUSPENSION\.md|_GLOBAL|_BRIEF|_MANIFEST"),
    "attribution": re.compile(r"Co-Authored-By|Generated with|claude\.com/claude-code|Claude Code", re.I),
    "ssh_key": re.compile(r"nousix_server_ed25519|ssh -i"),
    "user": re.compile(r"mattm@|mattsmcknight@"),
    "proc_run": re.compile(r"\bproc-[0-9a-f]{8}|k3d-nswe|k3s\b|argocd|kubectl|Tailscale"),
    "dag_runid": re.compile(r"design-chirp-r1"),
}
hyg_hits = {}
for name, rx in forbidden.items():
    hits = []
    for i, ln in enumerate(deliv_text.splitlines(), 1):
        for mm in rx.finditer(ln):
            hits.append((i, mm.group(0)))
    if hits:
        hyg_hits[name] = hits[:15]
results["HYGIENE"] = (not hyg_hits, {"hits": hyg_hits})

# ---------------- report ----------------
print("=" * 72)
print("INDEPENDENT RELEASE-BAR GATE VERIFICATION")
print("=" * 72)
allpass = True
order = ["BAR_RANGE_RESPECTED", "NO_BAR_COLLISION", "GATING_REQ_COVERAGE",
         "BAR_TESTABLE", "BAR_STAGED", "SURFACE_GAP_RECORDED",
         "THREE_SECTIONS_PRESENT", "HYGIENE"]
for k in order:
    ok, ev = results[k]
    allpass = allpass and ok
    print(f"\n[{'PASS' if ok else 'FAIL'}] {k}")
    print(json.dumps(ev, indent=2, ensure_ascii=False, default=list))
print("\n" + "=" * 72)
print("TOTAL BARS (fragments):", len(all_frag))
print("REGISTER BARS:", len(reg))
print("GATING TOTAL:", sum(gating_info[a]["gating"] for a in AREAS))
print("OVERALL VERDICT:", "ALL PASS" if allpass else "FAILURES PRESENT")
print("=" * 72)
