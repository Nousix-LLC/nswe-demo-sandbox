#!/usr/bin/env python3
"""Synthesis-gate verification for SUBTASK_bar_ux: assert the 8 subtree identities
against the assembled bar-ux.md and the five spoke sub-fragments. Pure read-only cross-check."""
import re, sys

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_release_bar/SUBTASK_bar_ux"
VOCAB = {"manual_user_check", "automated_test", "inspection", "operational_check"}
STAGES = {"usable_early", "releasable"}

SPOKES = {
    "ia":        (f"{BASE}/SUBTASK_bar_ux_ia/outputs/bar-ux-ia.md",                 200, 214),
    "visual":    (f"{BASE}/SUBTASK_bar_ux_visual/outputs/bar-ux-visual.md",         215, 229),
    "screens":   (f"{BASE}/SUBTASK_bar_ux_screens/outputs/bar-ux-screens.md",       230, 264),
    "responsive":(f"{BASE}/SUBTASK_bar_ux_responsive/outputs/bar-ux-responsive.md", 265, 274),
    "a11y":      (f"{BASE}/SUBTASK_bar_ux_a11y/outputs/bar-ux-a11y.md",             275, 294),
}
ASSEMBLED = f"{BASE}/outputs/bar-ux.md"

# release-gating REQ-UX sets per spoke (from contracts/bar_ux_partition.yaml)
GATING = {
    "ia":        [f"{n:03d}" for n in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,16,17,18]],
    "visual":    [f"{n:03d}" for n in [20,21,22,25,26,27,28,29,31,32,33,34,35,36,37,38,39]],
    "screens":   [f"{n:03d}" for n in list(range(40,57))+list(range(58,64))+list(range(65,71))+list(range(73,78))+[79]+list(range(82,90))],
    "responsive":[f"{n:03d}" for n in range(90,100)],
    "a11y":      [f"{n:03d}" for n in [100,101,102,103,104]+list(range(106,120))],
}
NONGATING = {f"{n:03d}" for n in [15,19,23,24,30,57,64,71,72,78,80,81,105]}

def parse_blocks(path):
    """Return {bar_id: {'refs': set(UX ids), 'vm': str|None, 'stage': str|None}}."""
    txt = open(path, encoding="utf-8").read()
    blocks = {}
    # split on headings that start a BAR block: '### BAR-NNN' or '## BAR-NNN'
    parts = re.split(r'(?m)^#{2,3}\s+(BAR-\d{3})\b', txt)
    # parts: [pre, id1, body1, id2, body2, ...]
    for i in range(1, len(parts), 2):
        bid = parts[i]
        body = parts[i+1]
        # stop body at next '---' section-ish? keep whole until next heading already handled by split
        refs = set(re.findall(r'REQ-UX-(\d{3})', body.split('\n## ')[0]))
        vm = None
        m = re.search(r'\*\*verification_method\*\*:\s*([a-z_]+)', body)
        if m: vm = m.group(1)
        stage = None
        ms = re.findall(r'\*\*stage\*\*:\s*([a-z_]+)', body)
        mps = re.findall(r'\*\*proposed_stage\*\*:\s*([a-z_]+)', body)
        allstage = ms + mps
        # only take the first stage occurrence belonging to this block (before any next subsection)
        head = body.split('\n### ')[0].split('\n## ')[0]
        hs = re.findall(r'\*\*(?:stage|proposed_stage)\*\*:\s*([a-z_]+)', head)
        if hs: stage = hs[0]; stagecount = len(hs)
        else: stage = None; stagecount = 0
        blocks[bid] = {"refs": refs, "vm": vm, "stage": stage, "stagecount": stagecount,
                       "vm_all": re.findall(r'\*\*verification_method\*\*:\s*([a-z_]+)', head)}
    return blocks

errors, notes = [], []

spoke_blocks = {}
for name,(path,lo,hi) in SPOKES.items():
    b = parse_blocks(path)
    spoke_blocks[name] = b
    for bid in b:
        n = int(bid.split('-')[1])
        if not (lo <= n <= hi):
            errors.append(f"[RANGE] {name}: {bid} outside {lo}..{hi}")

asm = parse_blocks(ASSEMBLED)

# Identity 1: UX_BAR_RANGE_RESPECTED (checked above for spokes); assembled ids also must sit in 200..299
for bid in asm:
    n = int(bid.split('-')[1])
    if not (200 <= n <= 299):
        errors.append(f"[RANGE] assembled {bid} outside 200..299")

# Identity 2: UX_NO_BAR_COLLISION — union of spoke ids distinct and == assembled ids
union = {}
for name,b in spoke_blocks.items():
    for bid in b:
        if bid in union:
            errors.append(f"[COLLISION] {bid} in both {union[bid]} and {name}")
        union[bid] = name
asm_ids = set(asm.keys())
spoke_ids = set(union.keys())
missing = spoke_ids - asm_ids
extra = asm_ids - spoke_ids
if missing: errors.append(f"[ASSEMBLY] spoke BARs missing from bar-ux.md: {sorted(missing)}")
if extra:
    # extra are synthesis cross-cutting 295..299 — allowed only in that range
    for bid in extra:
        n=int(bid.split('-')[1])
        if not (295<=n<=299):
            errors.append(f"[ASSEMBLY] bar-ux.md has {bid} not from any spoke and not cross-cutting 295..299")
        else:
            notes.append(f"cross-cutting minted: {bid}")

# Identity 4: UX_BAR_TESTABLE — vm in vocab, >=1 REQ ref; and assembled matches spoke vm
for bid in sorted(asm_ids):
    a = asm[bid]
    if a["vm"] not in VOCAB:
        errors.append(f"[TESTABLE] {bid} verification_method={a['vm']!r} not in vocab")
    if len(a["vm_all"])!=1:
        errors.append(f"[TESTABLE] {bid} has {len(a['vm_all'])} verification_method lines")
    if not a["refs"]:
        # some bars reference only REQ-PROD; check raw for any REQ-
        errors.append(f"[TESTABLE] {bid} references no REQ-UX-* (check REQ-PROD-only)")

# Identity 5: UX_BAR_STAGED — exactly one stage per assembled BAR, in vocab
for bid in sorted(asm_ids):
    a = asm[bid]
    if a["stagecount"]!=1:
        errors.append(f"[STAGED] {bid} has {a['stagecount']} stage lines (want 1)")
    if a["stage"] not in STAGES:
        errors.append(f"[STAGED] {bid} stage={a['stage']!r} not in {STAGES}")

# Cross-check assembled vs spoke: refs, vm, and stage reconciliation
stage_changes = []
for bid in sorted(spoke_ids):
    name = union[bid]
    s = spoke_blocks[name][bid]
    a = asm.get(bid)
    if not a: continue
    if s["refs"] != a["refs"]:
        errors.append(f"[REWRITE] {bid} refs differ spoke={sorted(s['refs'])} asm={sorted(a['refs'])}")
    if s["vm"] != a["vm"]:
        errors.append(f"[REWRITE] {bid} vm differ spoke={s['vm']} asm={a['vm']}")
    sstage = s["stage"]
    if sstage and a["stage"] and sstage != a["stage"]:
        stage_changes.append(f"{bid}: {name} proposed {sstage} -> assembled {a['stage']}")

# Identity 3 + 7: UX_GATING_REQ_COVERAGE + UX_COVERAGE_NOTE_PRESENT
# Build covered-set = every REQ-UX referenced by any assembled BAR
covered = set()
for bid,a in asm.items():
    covered |= a["refs"]
all_gating = set()
for name,g in GATING.items():
    all_gating |= set(g)
uncovered = all_gating - covered
if uncovered:
    errors.append(f"[COVERAGE] gating REQ-UX not referenced by any BAR: {sorted(uncovered)}")
# coverage note present?
asmtxt = open(ASSEMBLED, encoding="utf-8").read()
if "Coverage note" not in asmtxt and "coverage note" not in asmtxt:
    errors.append("[COVERAGE_NOTE] no coverage note heading found")

# Identity 6: UX_NONGATING_EXCLUDED — no BAR justified SOLELY by a non-gating REQ-UX
for bid,a in asm.items():
    if a["refs"] and a["refs"] <= NONGATING:
        errors.append(f"[NONGATING] {bid} justified solely by non-gating {sorted(a['refs'])}")

# Identity 8: UX_HYGIENE
hy = []
for pat,desc in [(r'100\.90\.75\.93',"host IP"),(r'ssh ',"ssh"),(r'/home/',"host path"),
                 (r'kubectl',"kubectl"),(r'SYNTHESIS\.md',"synthesis ref"),(r'SUSPENSION\.md',"suspension ref"),
                 (r'taskflow',"taskflow path"),(r'SUBTASK_',"subtask slug"),(r'Co-Authored-By',"attribution"),
                 (r'Generated with',"attribution"),(r'Claude',"attribution"),(r'_BRIEF',"brief ref"),(r'_GLOBAL',"global ref")]:
    if re.search(pat, asmtxt):
        hy.append(desc)
if hy:
    errors.append(f"[HYGIENE] bar-ux.md contains: {hy}")

# counts
print(f"spoke BAR count: {len(spoke_ids)} ; assembled BAR count: {len(asm_ids)}")
print(f"gating REQ-UX total: {len(all_gating)} (expect 106) ; covered: {len(covered & all_gating)}")
print(f"cross-cutting (295..299) minted: {sorted([b for b in asm_ids if 295<=int(b.split('-')[1])<=299])}")
if stage_changes:
    print("STAGE RECONCILIATIONS (spoke proposal -> assembled):")
    for c in stage_changes: print("  "+c)
else:
    print("stage reconciliations: none (every assembled stage equals its spoke's proposal)")
print()
if errors:
    print("FAIL — identity violations:")
    for e in errors: print("  "+e)
    sys.exit(1)
else:
    print("PASS — all 8 identities hold with evidence above.")
    for n in notes: print("  note: "+n)
    sys.exit(0)
