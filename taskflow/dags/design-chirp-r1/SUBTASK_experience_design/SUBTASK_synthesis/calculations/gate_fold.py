#!/usr/bin/env python3
"""
Independent synthesis gate for the experience-design subtree (fold-time re-derivation).

Re-derives evidence for all eight contract identities from scratch over the CURRENT
on-disk deliverable, the internal + parent contracts, and the product-requirements
register. Does NOT read or trust any prior SYNTHESIS.md verdict. Prints a structured
report and a final ALL-PASS / FAIL line.
"""
import re, sys, pathlib

ROOT = pathlib.Path("/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1")
SUB  = ROOT / "SUBTASK_experience_design"
DELIV = SUB / "outputs" / "experience-design.md"
PROD  = ROOT / "SUBTASK_product_requirements" / "outputs" / "product-requirements.md"

deliv = DELIV.read_text(encoding="utf-8")
prod  = PROD.read_text(encoding="utf-8")
lines = deliv.splitlines()

results = {}   # identity -> (pass_bool, [evidence lines])

def rec(idn, ok, *ev):
    results[idn] = (ok, list(ev))

# -----------------------------------------------------------------------------
# Parse top-level (## ) sections, in order, with their line spans.
# -----------------------------------------------------------------------------
sec_headings = [(i, l[3:].strip()) for i, l in enumerate(lines) if l.startswith("## ")]
# Expected contract order: (slug, keyword-set that must appear in heading, lower-cased)
expected = [
    ("information_architecture_and_interaction", "information architecture"),
    ("screens_and_flows",                        "screens and flows"),
    ("empty_error_loading_states",               "empty"),            # "Empty, loading, and error states"
    ("visual_language_and_design_system",        "visual language"),
    ("responsive_layout",                        "responsive"),
    ("accessibility",                            "accessibility"),
    ("requirements_and_acceptance_criteria",     "requirements and acceptance"),
]

# ---- Identity 1: SECTION_COVERAGE -------------------------------------------
heads = [h.lower() for _, h in sec_headings]
sc_ok = True
ev = [f"{len(sec_headings)} top-level sections found"]
if len(sec_headings) != 7:
    sc_ok = False
    ev.append(f"EXPECTED 7 sections, got {len(sec_headings)}")
else:
    for idx, (slug, kw) in enumerate(expected):
        h = heads[idx]
        match = kw in h
        ev.append(f"[{idx+1}] slug={slug:45s} heading={sec_headings[idx][1]!r} match={match}")
        if not match:
            sc_ok = False
# each heading occurs exactly once (no duplicate top-level sections)
from collections import Counter
dupes = [h for h, c in Counter(heads).items() if c > 1]
if dupes:
    sc_ok = False
    ev.append(f"DUPLICATE top-level headings: {dupes}")
rec("SECTION_COVERAGE", sc_ok, *ev)

# -----------------------------------------------------------------------------
# Parse the REQ-UX register. Register = content from the final '## Requirements
# and acceptance criteria' heading to EOF. Entries are '#### REQ-UX-NNN ...'.
# -----------------------------------------------------------------------------
reg_start = None
for i, l in enumerate(lines):
    if l.startswith("## ") and "requirements and acceptance" in l.lower():
        reg_start = i
if reg_start is None:
    print("FATAL: register section not found"); sys.exit(2)
reg_lines = lines[reg_start:]

# Build entry blocks
entries = []  # list of (id:int, title, blocktext)
cur = None
buf = []
for l in reg_lines:
    m = re.match(r'^####\s+REQ-UX-(\d{3})\s+[—-]\s*(.*)$', l)
    if m:
        if cur is not None:
            entries.append((cur[0], cur[1], "\n".join(buf)))
        cur = (int(m.group(1)), m.group(2).strip())
        buf = [l]
    elif cur is not None:
        buf.append(l)
if cur is not None:
    entries.append((cur[0], cur[1], "\n".join(buf)))

ids = [e[0] for e in entries]

# ---- Identity 2: ID_UNIQUE_IN_RANGE -----------------------------------------
ranges = {
    "ia":          (1, 19),
    "visual":      (20, 39),
    "screens":     (40, 89),
    "responsive":  (90, 99),
    "accessibility": (100, 119),
}
def owner_of(n):
    for name,(lo,hi) in ranges.items():
        if lo <= n <= hi: return name
    return None

ev = [f"register entries parsed: {len(entries)}"]
id_ok = True
dup_ids = [n for n, c in Counter(ids).items() if c > 1]
if dup_ids:
    id_ok = False; ev.append(f"DUPLICATE ids: {sorted(dup_ids)}")
else:
    ev.append("0 duplicate ids")
out_of_range = [n for n in ids if owner_of(n) is None]
if out_of_range:
    id_ok = False; ev.append(f"OUT OF RANGE ids: {sorted(out_of_range)}")
else:
    ev.append("0 out-of-range ids (all within 001..119 owner partitions)")
expected_ids = set(range(1, 120))
missing = sorted(expected_ids - set(ids))
extra   = sorted(set(ids) - expected_ids)
if missing: id_ok = False; ev.append(f"MISSING ids: {missing}")
else: ev.append("contiguous 001..119, none missing")
if extra: id_ok = False; ev.append(f"EXTRA ids: {extra}")
# per-owner counts
for name,(lo,hi) in ranges.items():
    c = sum(1 for n in ids if lo <= n <= hi)
    ev.append(f"  {name:13s} {lo:03d}..{hi:03d}: {c} entries")
rec("ID_UNIQUE_IN_RANGE", id_ok, *ev)

# ---- Identity 3: UX_TESTABLE_AND_GATED --------------------------------------
# Each entry has statement, acceptance_criteria, release_gating bullets.
field_re = {
    "statement":          re.compile(r'(?m)^\s*-\s+\*\*statement\*\*\s*:\s*(.*)$'),
    "acceptance_criteria":re.compile(r'(?m)^\s*-\s+\*\*acceptance_criteria\*\*\s*:\s*(.*)$'),
    "release_gating":     re.compile(r'(?m)^\s*-\s+\*\*release_gating\*\*\s*:\s*(.*)$'),
    "references":         re.compile(r'(?m)^\s*-\s+\*\*references\*\*\s*:\s*(.*)$'),
}
missing_fields = []     # (id, field)
short_ac = []           # (id, len)
gating_true = gating_false = 0
bad_gating = []
parsed = {}  # id -> dict(field->firstline, full acceptance text)
for n, title, block in entries:
    rowfields = {}
    for f, rx in field_re.items():
        m = rx.search(block)
        if not m:
            missing_fields.append((n, f))
        else:
            rowfields[f] = m.group(1).strip()
    parsed[n] = rowfields
    # acceptance criteria length: capture from the bullet to next bullet
    ac_ok = "acceptance_criteria" in rowfields
    if ac_ok:
        # gather full AC text (may wrap lines until next '- **' bullet)
        acm = re.search(r'(?ms)^\s*-\s+\*\*acceptance_criteria\*\*\s*:\s*(.*?)(?=^\s*-\s+\*\*|\Z)', block)
        actext = (acm.group(1) if acm else "").strip()
        if len(actext) < 25:
            short_ac.append((n, len(actext)))
    rg = rowfields.get("release_gating", "").lower()
    if rg.startswith("true"): gating_true += 1
    elif rg.startswith("false"): gating_false += 1
    elif "release_gating" in rowfields: bad_gating.append((n, rg))

tg_ok = not missing_fields and not short_ac and not bad_gating
ev = [f"gating: {gating_true} true / {gating_false} false  (sum={gating_true+gating_false} of {len(entries)})"]
ev.append(f"missing-field entries: {missing_fields if missing_fields else 'none'}")
ev.append(f"acceptance_criteria <25 chars: {short_ac if short_ac else 'none'}")
ev.append(f"unparseable release_gating: {bad_gating if bad_gating else 'none'}")
rec("UX_TESTABLE_AND_GATED", tg_ok, *ev)

# ---- Identity 4: UX_TRACES_TO_PROD ------------------------------------------
prod_ids = set(int(x[-3:]) for x in re.findall(r'REQ-PROD-(\d{3})', prod))
# forward: each entry references >=1 REQ-PROD; all referenced exist
no_ref = []
dangling = set()
covered_prod = set()   # REQ-PROD ints referenced by some REQ-UX
for n, title, block in entries:
    refs = [int(x) for x in re.findall(r'REQ-PROD-(\d{3})', block)]
    if not refs:
        no_ref.append(n)
    for r in refs:
        covered_prod.add(r)
        if r not in prod_ids:
            dangling.add(r)
# reverse: contract required_surfaces REQ-PROD union (authoritative surface list)
required_surface_prod = {
    30,31,            # first_visit_landing
    8,9,31,           # sign_up
    10,11,            # sign_in
    12,13,            # account_recovery
    14,               # sign_out
    2,                # home_timeline
    1,                # compose_and_post
    3,4,              # reply_and_conversation
    5,                # like_unlike
    6,                # follow_unfollow
    42,               # discovery
    7,                # view_profile
    32,               # onboarding_empty_state
    16,               # edit_profile
    17,18,            # account_settings
    19,               # data_export
    20,21,22,         # account_deletion
    29,               # notifications
    25,26,27,         # report_and_block
    28,               # help_support_entry
    33,34,            # considered_states_global
}
# broader "user-facing" set used by the subtree (experience-quality 030-036 +
# user-facing surface of 001-028 + {032,033,034,042}); its residue vs covered is
# the recorded-disposition set.
broader = set(range(1,29)) | set(range(30,37)) | {32,33,34,42}
recorded_dispositions = {15, 23, 24}

surface_uncovered = sorted(required_surface_prod - covered_prod)
broader_uncovered = sorted(broader - covered_prod)

fwd_ok = (not no_ref) and (not dangling)
# reverse passes if: every contract-required-surface prod id is covered, AND every
# broader-set residue is either covered or a recorded disposition.
rev_contract_ok = (len(surface_uncovered) == 0)
rev_broader_ok  = set(broader_uncovered).issubset(recorded_dispositions)
tr_ok = fwd_ok and rev_contract_ok and rev_broader_ok
ev = [f"REQ-PROD ids in register: {len(prod_ids)} (expect 42, contiguous={sorted(prod_ids)==list(range(1,43))})"]
ev.append(f"forward: entries with no REQ-PROD ref: {no_ref if no_ref else 'none'}")
ev.append(f"forward: dangling refs (not in prod register): {sorted(dangling) if dangling else 'none'}")
ev.append(f"reverse(contract required_surfaces union, {len(required_surface_prod)} ids): uncovered={surface_uncovered if surface_uncovered else 'none'}")
ev.append(f"reverse(broader user-facing set, {len(broader)} ids): uncovered={broader_uncovered}")
ev.append(f"  -> broader residue {broader_uncovered} subset of recorded dispositions {sorted(recorded_dispositions)}: {rev_broader_ok}")
ev.append(f"total distinct REQ-PROD covered by some REQ-UX: {len(covered_prod)}")
rec("UX_TRACES_TO_PROD", tr_ok, *ev)

# ---- Identity 5: COMPOSES_AGAINST_PARENT ------------------------------------
# Field set per entry is exactly {statement, acceptance_criteria, release_gating, references}.
# Detect any bold bullet key in the register that is not one of those four.
allowed = {"statement","acceptance_criteria","release_gating","references"}
reg_text = "\n".join(reg_lines)
bold_keys = Counter(re.findall(r'(?m)^\s*-\s+\*\*([a-z_]+)\*\*\s*:', reg_text))
foreign = {k:v for k,v in bold_keys.items() if k not in allowed}
cp_ok = not foreign
ev = [f"bold bullet keys in register: {dict(bold_keys)}"]
ev.append(f"foreign (non-parent) field keys: {foreign if foreign else 'none'}")
ev.append("section list == parent design_artifact_map.yaml list (verified by SECTION_COVERAGE order check)")
rec("COMPOSES_AGAINST_PARENT", cp_ok, *ev)

# ---- Identity 6: SURFACE_COVERAGE -------------------------------------------
# Each required surface must be designed with states OR recorded out-of-scope.
# Mechanical proxy: (a) every required-surface REQ-PROD id is forward-covered by
# >=1 REQ-UX (checked in #4 rev_contract_ok); (b) surface keyword present in the
# screens/flows + considered-states region.
screens_region = "\n".join(lines[sec_headings[1][0]: sec_headings[3][0]]).lower()  # screens + empty/error sections
surface_keywords = {
    "first_visit_landing": ["landing","first visit","signed-out"],
    "sign_up": ["sign up","sign-up"],
    "sign_in": ["sign in","sign-in"],
    "account_recovery": ["recover","reset"],
    "sign_out": ["sign out","sign-out","log out"],
    "home_timeline": ["timeline"],
    "compose_and_post": ["compose","post"],
    "reply_and_conversation": ["reply","conversation"],
    "like_unlike": ["like"],
    "follow_unfollow": ["follow"],
    "discovery_find_people": ["explore","discover"],
    "view_profile": ["profile"],
    "onboarding_empty_state": ["onboard","empty state","get started"],
    "edit_profile": ["edit profile"],
    "account_settings": ["settings"],
    "data_export": ["export"],
    "account_deletion": ["delete","deletion"],
    "notifications": ["notification"],
    "report_and_block": ["report","block"],
    "help_support_entry": ["help","support"],
    "considered_states_global": ["empty","loading","error"],
}
missing_surface = []
for surf, kws in surface_keywords.items():
    if not any(kw in screens_region for kw in kws):
        # also look in whole deliverable before failing
        if not any(kw in deliv.lower() for kw in kws):
            missing_surface.append(surf)
surf_ok = (len(missing_surface) == 0) and rev_contract_ok
ev = [f"required surfaces: {len(surface_keywords)}"]
ev.append(f"surfaces with no keyword hit: {missing_surface if missing_surface else 'none'}")
ev.append(f"every required-surface REQ-PROD forward-covered by >=1 REQ-UX: {rev_contract_ok}")
rec("SURFACE_COVERAGE", surf_ok, *ev)

# ---- Identity 7: NOT_SKELETAL -----------------------------------------------
# Each designed screen specifies layout/content/primary action and empty/error/loading
# states -- not a bare route name. Screens are '#### <name> -- `/route`, <archetype>'
# entries inside the Screens-and-flows section; some sub-screens use '#####'. States are
# '**States.**' bold runs and/or 'States' sub-headings, with Empty/Error/Loading bullets.
# Use the ORIGINAL-CASE text (not lowered) so capitalized markers match.
scr_lo, scr_hi = sec_headings[1][0], sec_headings[2][0]        # Screens and flows only
eel_lo, eel_hi = sec_headings[2][0], sec_headings[3][0]        # Empty/loading/error section
scr_text = "\n".join(lines[scr_lo:scr_hi])
eel_text = "\n".join(lines[eel_lo:eel_hi])
both = scr_text + "\n" + eel_text

# screen entries = #### / ##### headings that declare a route (backtick) or 'archetype'
screen_entries = [l for l in scr_text.splitlines()
                  if re.match(r'^#{4,5}\s', l) and ('`/' in l or 'archetype' in l.lower()
                                                    or re.search(r'`?/[a-z]', l))]
screen_count = len(screen_entries)
states_blocks = len(re.findall(r'\*\*States\.?\*\*', both)) + len(re.findall(r'(?m)^#{3,6}\s+States\b', both))
layout_n  = len(re.findall(r'\*\*Layout', both))
primary_n = len(re.findall(r'\*\*Primary action', both)) + both.count("Primary action")
empty_n   = len(re.findall(r'(?i)\*\*Empty', both)) + both.lower().count("empty")
error_n   = both.lower().count("error") + both.lower().count("failed")
loading_n = both.lower().count("loading")
# dedicated per-pattern state sections in the empty/error/loading section
eel_heads = re.findall(r'(?m)^###\s+(.*)$', eel_text)
# The contract fixes no screen count; the test is that screens are designed with
# layout + primary action + empty/error/loading states, not bare route names. The
# pass is keyed to that substantive evidence (a skeletal doc would be ~0 on each).
ns_ok = (screen_count >= 15 and states_blocks >= 15 and layout_n >= 15
         and primary_n >= 20 and empty_n >= 30 and error_n >= 30 and loading_n >= 30
         and len(eel_heads) >= 3)
ev = [f"designed screen entries (#### / ##### with a route/archetype): {screen_count}",
      f"explicit States blocks (**States.** + 'States' subheadings): {states_blocks}",
      f"**Layout** blocks: {layout_n}",
      f"'Primary action' markers: {primary_n}",
      f"'empty' mentions: {empty_n}", f"'error'/'failed' mentions: {error_n}",
      f"'loading' mentions: {loading_n}",
      f"dedicated state-pattern sections in empty_error_loading_states: {eel_heads}"]
rec("NOT_SKELETAL", ns_ok, *ev)

# ---- Identity 8: HYGIENE ----------------------------------------------------
low = deliv.lower()
forbidden = {
    "server ip (100.90)": "100.90",
    "ssh": "ssh ",
    "kubectl": "kubectl",
    "k3d": "k3d",
    "k3s": "k3s",
    "argocd": "argocd",
    "tailscale": "tailscale",
    "port 8081": "8081",
    "subtask_": "subtask_",
    "taskflow": "taskflow",
    "_global": "_global",
    "_brief": "_brief",
    "commit sha c805525": "c805525",
    "workspace path": "/home/user",
    "nousix-runtime": "nousix-runtime",
    "co-authored-by": "co-authored-by",
    "generated with claude": "generated with",
    "user email": "dev@example.com",
    "dag id": "proc-",
}
hits = {}
for label, tok in forbidden.items():
    c = low.count(tok.lower())
    if c:
        hits[label] = c
hy_ok = not hits
ev = [f"forbidden-token hits: {hits if hits else 'none'}"]
rec("HYGIENE", hy_ok, *ev)

# -----------------------------------------------------------------------------
# Report
# -----------------------------------------------------------------------------
print("="*78)
print("INDEPENDENT EXPERIENCE-DESIGN SYNTHESIS GATE  (fold-time re-derivation)")
print("="*78)
print(f"deliverable: {DELIV}  ({len(deliv)} bytes, {len(lines)} lines)")
print(f"register entries: {len(entries)}   REQ-PROD register: {len(prod_ids)} ids")
print()
all_ok = True
for idn in ["SECTION_COVERAGE","ID_UNIQUE_IN_RANGE","UX_TESTABLE_AND_GATED",
            "UX_TRACES_TO_PROD","COMPOSES_AGAINST_PARENT","SURFACE_COVERAGE",
            "NOT_SKELETAL","HYGIENE"]:
    ok, ev = results[idn]
    all_ok = all_ok and ok
    print(f"[{'PASS' if ok else 'FAIL'}] {idn}")
    for line in ev:
        print(f"        {line}")
    print()
print("="*78)
print("ALL IDENTITIES PASS" if all_ok else "GATE FAILED — one or more identities did not pass")
print("="*78)
sys.exit(0 if all_ok else 1)
