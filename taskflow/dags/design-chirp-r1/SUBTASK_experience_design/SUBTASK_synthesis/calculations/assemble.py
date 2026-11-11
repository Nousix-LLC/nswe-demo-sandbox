#!/usr/bin/env python3
"""Deterministic assembly of experience-design.md from the five sibling outputs.

Rules (contract ux_section_and_id_map.yaml, sections_in_order):
  1 information_architecture_and_interaction  <- ia-interaction.md prose
  2 screens_and_flows                         <- screens-flows.md  '## Screens and flows'
  3 empty_error_loading_states                <- screens-flows.md  '## Empty, loading, and error states'
  4 visual_language_and_design_system         <- visual-system.md prose (Component library demoted +1 to nest)
  5 responsive_layout                         <- responsive.md prose
  6 accessibility                             <- accessibility.md prose
  7 requirements_and_acceptance_criteria      <- consolidated REQ-UX-001..119 (id order), verbatim blocks

No prose or requirement wording is altered. Only: per-file lead intros are dropped, the one
'## Component library' subtree is demoted one level so it nests under the visual section, and the
five register portions are concatenated in id order under one consolidated section.
"""
import re, sys

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_experience_design"
OUT  = BASE + "/outputs/experience-design.md"

IA   = BASE + "/SUBTASK_ia_interaction/outputs/ia-interaction.md"
VIS  = BASE + "/SUBTASK_visual_system/outputs/visual-system.md"
SCR  = BASE + "/SUBTASK_screens_flows/outputs/screens-flows.md"
RES  = BASE + "/SUBTASK_responsive/outputs/responsive.md"
ACC  = BASE + "/SUBTASK_accessibility/outputs/accessibility.md"

REG_HEAD = re.compile(r'^#{2,6}\s+Requirements and acceptance criteria', re.M)
UX_HEAD  = re.compile(r'^####\s+REQ-UX-(\d{3})\b', re.M)

def read(p):
    with open(p, encoding="utf-8") as f:
        return f.read()

def split_prose_register(text):
    """prose = everything before the first 'Requirements and acceptance criteria' heading."""
    m = REG_HEAD.search(text)
    if not m:
        sys.exit("no register header in a source")
    return text[:m.start()].rstrip(), text[m.start():]

def ux_blocks(register_text):
    """list of (num, block_text) for every #### REQ-UX-NNN block in the register portion."""
    heads = [(m.start(), int(m.group(1))) for m in UX_HEAD.finditer(register_text)]
    out = []
    for i, (pos, num) in enumerate(heads):
        end = heads[i+1][0] if i + 1 < len(heads) else len(register_text)
        out.append((num, register_text[pos:end].rstrip()))
    return out

def demote(block):
    """Add one '#' to every ATX heading line in block (so a '## x' subtree nests a level deeper)."""
    return re.sub(r'^(#{1,5}) ', r'#\1 ', block, flags=re.M)

# ---- collect all REQ-UX blocks from all five register portions -------------------------------
all_ux = {}
prose = {}
for key, path in [("ia", IA), ("vis", VIS), ("scr", SCR), ("res", RES), ("acc", ACC)]:
    text = read(path)
    pr, reg = split_prose_register(text)
    prose[key] = pr
    for num, blk in ux_blocks(reg):
        if num in all_ux:
            sys.exit(f"duplicate REQ-UX-{num:03d} across sources")
        all_ux[num] = blk

# ---- section 1: IA (prose leads with '## Information architecture and interaction model') -----
ia_sec = prose["ia"]

# ---- sections 2 & 3: screens-flows -> drop '# ' file title+intro, split at empty/error heading -
scr_text = prose["scr"]
m_sf = re.search(r'^## Screens and flows\s*$', scr_text, re.M)
m_ee = re.search(r'^## Empty, loading, and error states\s*$', scr_text, re.M)
if not (m_sf and m_ee):
    sys.exit("screens-flows section headings not found")
screens_sec = scr_text[m_sf.start():m_ee.start()].rstrip()
states_sec  = scr_text[m_ee.start():].rstrip()

# ---- section 4: visual -> keep visual-language part; demote the Component library subtree +1 ---
vis_text = prose["vis"]
m_cl = re.search(r'^## Component library\s*$', vis_text, re.M)
if not m_cl:
    sys.exit("visual Component library heading not found")
vis_lang = vis_text[:m_cl.start()].rstrip()
vis_cl   = demote(vis_text[m_cl.start():].rstrip())
vis_sec  = vis_lang + "\n\n" + vis_cl

# ---- sections 5 & 6 ---------------------------------------------------------------------------
res_sec = prose["res"]
acc_sec = prose["acc"]

# ---- section 7: consolidated register ---------------------------------------------------------
nums = sorted(all_ux)
reg_body = "\n\n".join(all_ux[n] for n in nums)

INTRO = (
"# chirp — Experience Design\n\n"
"How chirp looks and behaves to the people who use it: the information architecture and interaction "
"model, a designed screen for every journey a releasable chirp needs, the product-wide empty, loading, "
"and error behaviour, the visual language and component library, responsive behaviour from a phone "
"upward, the accessibility standard, and the full `REQ-UX-*` requirements register that makes each of "
"these testable on the live product.\n\n"
"This document takes chirp from a three-screen skeleton — timeline, compose, and profile — to a "
"designed, releasable consumer web product: the full account lifecycle, onboarding, settings, safety, "
"notifications, data export and deletion, and considered empty, error, and loading states throughout. "
"The requirements register at the end is the single source of testable acceptance criteria; each "
"requirement carries a release-gating flag and traces to the product requirements it serves. The "
"document is design — what the product must look like and do — and leaves the build to the "
"implementation that follows.\n"
)

REG_INTRO = (
"## Requirements and acceptance criteria\n\n"
"The complete `REQ-UX-*` register for the experience design, consolidated across information "
"architecture (`REQ-UX-001..019`), the visual language and component library (`REQ-UX-020..039`), "
"screens and flows (`REQ-UX-040..089`), responsive behaviour (`REQ-UX-090..099`), and accessibility "
"(`REQ-UX-100..119`). Every entry has a statement, an `acceptance_criteria` a person who never met the "
"author can check against the live product, a `release_gating` flag (a `false` flag carries its reason), "
"and the product requirement(s) it serves. Ids are unique and contiguous from `REQ-UX-001` to "
"`REQ-UX-119`.\n"
)

doc = "\n\n".join([
    INTRO.rstrip(),
    ia_sec,
    screens_sec,
    states_sec,
    vis_sec,
    res_sec,
    acc_sec,
    REG_INTRO.rstrip() + "\n\n" + reg_body,
]) + "\n"

# ---- in-script assertions ---------------------------------------------------------------------
assert nums == list(range(1, 120)), f"REQ-UX ids not 1..119 contiguous: missing={sorted(set(range(1,120))-set(nums))}"
for name in ["## Information architecture and interaction model",
             "## Screens and flows",
             "## Empty, loading, and error states",
             "## Visual language and design system",
             "## Responsive layout",
             "## Accessibility",
             "## Requirements and acceptance criteria"]:
    assert doc.count("\n" + name + "\n") >= 1 or doc.startswith(name) or ("\n"+name+"\n") in ("\n"+doc), f"missing section heading: {name}"

# order check: the seven required section headings appear once, in order
order = ["## Information architecture and interaction model",
         "## Screens and flows",
         "## Empty, loading, and error states",
         "## Visual language and design system",
         "## Responsive layout",
         "## Accessibility",
         "## Requirements and acceptance criteria"]
positions = [doc.index("\n" + h + "\n") if ("\n"+h+"\n") in doc else doc.index(h) for h in order]
assert positions == sorted(positions), f"section headings out of order: {positions}"

import os
os.makedirs(os.path.dirname(OUT), exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(doc)

print("WROTE", OUT)
print("bytes:", len(doc.encode("utf-8")))
print("REQ-UX count:", len(nums), "range", nums[0], "-", nums[-1])
print("section order positions:", positions)
# count top-level (##) headings for a sanity read
tops = re.findall(r'^## .+$', doc, re.M)
print("top-level (##) headings:", len(tops))
for t in tops:
    print("   ", t)
