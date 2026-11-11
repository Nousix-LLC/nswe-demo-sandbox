#!/usr/bin/env python3
# Verification of the screens-&-flows synthesis: mechanical identity checks against the authoritative tree.
# Reproducible: reads the five spoke outputs + the assembled deliverable, prints a per-check verdict.
# Run:  python3 -I verify_synthesis.py
import re, sys, os

BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))  # .../SUBTASK_screens_flows
SPOKES = {
    "get_in":               (f"{BASE}/SUBTASK_get_in/outputs/screens-get-in.md",                 range(40, 51)),
    "core_loop":            (f"{BASE}/SUBTASK_core_loop/outputs/screens-core-loop.md",           range(51, 65)),
    "account_lifecycle":    (f"{BASE}/SUBTASK_account_lifecycle/outputs/screens-account-lifecycle.md", range(65, 78)),
    "safety_notifications": (f"{BASE}/SUBTASK_safety_notifications/outputs/screens-safety-notifications.md", range(78, 86)),
    "considered_states":    (f"{BASE}/SUBTASK_considered_states/outputs/empty-error-loading-states.md",     range(86, 90)),
}
ASSEMBLED = f"{BASE}/outputs/screens-flows.md"

results = []
def check(name, ok, detail):
    results.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}: {detail}")

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def extract_entries(text):
    """Return dict id -> block text. An entry is a MARKDOWN HEADING (any level 2..6) whose text
    begins with a REQ-UX id — a mint, not a bare in-prose reference or a table row. The block runs
    to the next heading of any level."""
    out = {}
    lines = text.splitlines(keepends=True)
    idxs = []
    for i, ln in enumerate(lines):
        m = re.match(r'^#{2,6}\s+(REQ-UX-0\d\d)\b', ln)
        if m:
            idxs.append((i, m.group(1)))
    for n, (i, rid) in enumerate(idxs):
        j = len(lines)
        for k in range(i+1, len(lines)):
            if re.match(r'^#{2,6}\s', lines[k]):
                j = k; break
        out[rid] = "".join(lines[i:j])
    return out

def norm(s):
    return re.sub(r'\s+', ' ', s).strip()

def field_value(block, field):
    """Pull the text of a '- **field**: ...' bullet (through wrapped continuation lines)."""
    lines = block.splitlines()
    val, capturing = [], False
    for ln in lines:
        m = re.match(r'^\s*-\s+\*\*' + field + r'\*\*\s*:?\s*(.*)$', ln, re.I)
        if m:
            capturing = True; val.append(m.group(1)); continue
        if capturing:
            if re.match(r'^\s*-\s+\*\*\w', ln) or re.match(r'^#{1,6}\s', ln) or ln.strip() == "":
                break
            val.append(ln)
    return norm(" ".join(val))

# ---------- gather spoke register entries (only each spoke's own minted sub-range) ----------
spoke_entries = {}   # id -> (spoke, block)
spoke_minted = {}    # spoke -> set(ids)
for spoke, (path, rng) in SPOKES.items():
    txt = read(path)
    ents = extract_entries(txt)
    owned = {rid: blk for rid, blk in ents.items() if int(rid.split('-')[-1]) in rng}
    spoke_minted[spoke] = set(owned)
    for rid, blk in owned.items():
        spoke_entries[rid] = (spoke, blk)

atext = read(ASSEMBLED)
asm_entries = extract_entries(atext)

# ===== ID_UNIQUE_IN_RANGE =====
expected = {f"REQ-UX-{n:03d}" for n in range(40, 90)}
# per-spoke range correctness
range_ok = True; rdetail = []
for spoke, (path, rng) in SPOKES.items():
    want = {f"REQ-UX-{n:03d}" for n in rng}
    got = spoke_minted[spoke]
    rdetail.append(f"{spoke}:{len(got)}")
    if got != want:
        range_ok = False
        rdetail.append(f"  MISMATCH {spoke}: missing={sorted(want-got)} extra={sorted(got-want)}")
union = set(spoke_entries)
check("ID_UNIQUE_IN_RANGE/spoke_ranges", range_ok and union == expected,
      f"union={len(union)} expected=50 contiguous_040_089={union==expected}; per-spoke counts: {' '.join(rdetail)}")

# assembled register entries: exactly the 50, unique
asm_ids = set(asm_entries)
check("ID_UNIQUE_IN_RANGE/assembled", asm_ids == expected,
      f"assembled register entry headings = {len(asm_ids)}; equals 040..089 = {asm_ids==expected}; "
      f"missing={sorted(expected-asm_ids)} extra={sorted(asm_ids-expected)}")

# ===== FAITHFUL ASSEMBLY (no drift, no invention): each assembled entry's acceptance_criteria body
#       comes from its OWNING spoke file (normalized substring), proving assembly, not re-writing. =====
spoke_text = {sp: norm(read(p)) for sp, (p, _) in SPOKES.items()}
owner_of = {}
for sp, (_, rng) in SPOKES.items():
    for n in rng:
        owner_of[f"REQ-UX-{n:03d}"] = sp
drift = []
checked = 0
for rid in sorted(expected):
    ac = field_value(asm_entries.get(rid, ""), "acceptance_criteria")
    st = field_value(asm_entries.get(rid, ""), "statement")
    owner = owner_of[rid]
    probe = ac if len(ac) >= 20 else st
    if len(probe) < 20:
        drift.append(f"{rid}: no extractable acceptance_criteria/statement body"); continue
    checked += 1
    if probe not in spoke_text[owner]:
        # tolerate minor terminal punctuation differences by trimming
        if probe.rstrip('.') not in spoke_text[owner]:
            drift.append(f"{rid}: assembled body not found in owning spoke {owner}: {probe[:70]}")
check("FAITHFUL_ASSEMBLY", not drift,
      f"all 50 assembled entries' acceptance/statement bodies trace back verbatim to their owning spoke "
      f"({checked} bodies matched)" if not drift else f"{len(drift)} drift(s): " + " | ".join(drift[:6]))

# ===== UX_TESTABLE_AND_GATED (+ gating false reason) =====
missing_fields = []; gating_true = 0; gating_false = 0; false_no_reason = []
for rid in sorted(expected):
    blk = asm_entries.get(rid, "")
    low = blk.lower()
    for fld in ("statement", "acceptance_criteria", "release_gating"):
        if f"**{fld}**" not in blk:
            missing_fields.append(f"{rid}:{fld}")
    m = re.search(r'\*\*release_gating\*\*\s*:\s*\*?\*?\s*(true|false)', blk, re.I)
    if m:
        if m.group(1).lower() == "true":
            gating_true += 1
        else:
            gating_false += 1
            # require a reason on the same line or wording after false
            line = re.search(r'\*\*release_gating\*\*\s*:.*', blk, re.I).group(0)
            after = line.split(m.group(1), 1)[-1].strip(" .—-:")
            if len(after) < 8:
                false_no_reason.append(rid)
    else:
        missing_fields.append(f"{rid}:release_gating_value")
check("UX_TESTABLE_AND_GATED", not missing_fields and not false_no_reason,
      f"all 50 carry statement+acceptance_criteria+release_gating; gating true={gating_true} false={gating_false}; "
      f"missing_fields={missing_fields or 'none'}; false_without_reason={false_no_reason or 'none'}")

# ===== UX_TRACES_TO_PROD =====
no_trace = [rid for rid in sorted(expected)
            if not re.search(r'REQ-PROD-\d', asm_entries.get(rid, ""))]
check("UX_TRACES_TO_PROD", not no_trace,
      f"every register entry references >=1 REQ-PROD-*; without_trace={no_trace or 'none'}")

# ===== SECTION_PART_COVERAGE (order of the required headings — anchored to line-start at exact level) =====
heads = [
    (r'^##\s+Screens and flows',                     "## Screens and flows"),
    (r'^###\s+Getting in',                           "### Getting in"),
    (r'^###\s+The core loop',                        "### The core loop"),
    (r'^###\s+Account lifecycle',                    "### Account lifecycle"),
    (r'^###\s+Safety, notifications',                "### Safety, notifications"),
    (r'^##\s+Empty, error, and loading states',      "## Empty, error, and loading states"),
    (r'^##\s+Requirements and acceptance criteria',  "## Requirements and acceptance criteria"),
]
offs = []
for pat, label in heads:
    m = re.search(pat, atext, re.M)
    offs.append((label, m.start() if m else -1))
present = all(o != -1 for _, o in offs)
mono = present and [o for _, o in offs] == sorted(o for _, o in offs)
check("SECTION_PART_COVERAGE", mono,
      f"two sections present, four screen-parts in contract order then empty-states then register: {offs}")

# ===== HYGIENE =====
banned = ["taskflow", "SUBTASK_", "_GLOBAL", "_BRIEF", "workspace", "kubectl", "k3d", "argocd",
          "Co-Authored-By", "Claude Code", "100.90.75.93", "nousix_server", "mattm",
          "proc-", "SYNTHESIS.md", "/home/"]
hits = {}
for tok in banned:
    c = atext.count(tok)
    if c:
        hits[tok] = c
check("HYGIENE", not hits, f"forbidden-token scan of assembled deliverable: {hits or 'zero occurrences'}")

print("\n==== SUMMARY ====")
nfail = sum(1 for _, ok, _ in results if not ok)
print(f"{len(results)} checks, {nfail} failed")
sys.exit(1 if nfail else 0)
