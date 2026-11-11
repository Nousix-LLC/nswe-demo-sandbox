#!/usr/bin/env python3
"""Independent resume-time verification gate over the assembled experience-design.md.
Re-derives evidence for all eight experience-design subtree identities from the current
on-disk deliverable + the parent/internal contracts + the product-requirements register.
Authored by the resumed SUBTASK_synthesis node; does not trust the prior run's recorded output."""
import re, sys

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_experience_design"
DOC  = BASE + "/outputs/experience-design.md"
PROD = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_product_requirements/outputs/product-requirements.md"

doc  = open(DOC, encoding="utf-8").read()
fails = []

# contract: section order (parent design_artifact_map.yaml == internal ux_section_and_id_map order)
ORDER = ["## Information architecture and interaction model",
         "## Screens and flows",
         "## Empty, loading, and error states",
         "## Visual language and design system",
         "## Responsive layout",
         "## Accessibility",
         "## Requirements and acceptance criteria"]
# contract: id ranges per owning child
RANGES = [("ia_interaction",1,19),("visual_system",20,39),("screens_flows",40,89),
          ("responsive",90,99),("accessibility",100,119)]
def owner_of(n):
    for o,lo,hi in RANGES:
        if lo<=n<=hi: return o,lo,hi
    return None,None,None

print("="*78); print("RESUME-TIME GATE over assembled experience-design.md"); print("="*78)
print(f"deliverable bytes: {len(doc)}")

# ---- parse the consolidated REQ-UX register ---------------------------------------------------
reg_start = doc.index("## Requirements and acceptance criteria")
reg = doc[reg_start:]
HEAD = re.compile(r'^####\s+REQ-UX-(\d{3})\b', re.M)
heads = [(m.start(), int(m.group(1))) for m in HEAD.finditer(reg)]
blocks = {}
for i,(pos,num) in enumerate(heads):
    end = heads[i+1][0] if i+1<len(heads) else len(reg)
    blocks[num] = reg[pos:end]
nums = sorted(blocks)

# ---- [1] SECTION_COVERAGE ---------------------------------------------------------------------
counts = [len(re.findall(r'(?m)^'+re.escape(h)+r'\s*$', doc)) for h in ORDER]
pos = [doc.index(h) for h in ORDER]
once = all(c==1 for c in counts)
ordered = pos==sorted(pos)
print("\n[1] SECTION_COVERAGE")
print("   per-section occurrence counts:", counts)
print("   each exactly once:", once, " | strictly ascending (contract order):", ordered)
if not (once and ordered): fails.append("SECTION_COVERAGE")

# ---- [2] ID_UNIQUE_IN_RANGE -------------------------------------------------------------------
missing = sorted(set(range(1,120))-set(nums)); extra = sorted(set(nums)-set(range(1,120)))
dups = len(heads)-len(set(n for _,n in heads))
oor = [n for n in nums if not (owner_of(n)[1] and owner_of(n)[1] <= n <= owner_of(n)[2])]
print("\n[2] ID_UNIQUE_IN_RANGE")
print(f"   entries:{len(nums)} contiguous_1..119:{nums==list(range(1,120))} missing:{missing or 'NONE'} extra:{extra or 'NONE'} dup_headings:{dups} out_of_range:{oor or 'NONE'}")
if missing or extra or dups or oor: fails.append("ID_UNIQUE_IN_RANGE")

# ---- [3] UX_TESTABLE_AND_GATED ----------------------------------------------------------------
no_s=[];no_a=[];no_g=[];thin_a=[];gate={"true":0,"false":0}
for n,b in blocks.items():
    if not re.search(r'\*\*statement\*\*\s*:',b): no_s.append(n)
    ma=re.search(r'\*\*acceptance_criteria\*\*\s*:\s*(.+)',b)
    if not ma: no_a.append(n)
    elif len(ma.group(1).strip())<25: thin_a.append(n)   # hardening: flag trivially short AC
    mg=re.search(r'\*\*release_gating\*\*\s*:\s*(true|false)\b',b)
    if not mg: no_g.append(n)
    else: gate[mg.group(1)]+=1
print("\n[3] UX_TESTABLE_AND_GATED")
print(f"   missing statement:{no_s or 'NONE'} missing acceptance_criteria:{no_a or 'NONE'} missing gate:{no_g or 'NONE'} suspiciously-thin AC:{thin_a or 'NONE'}")
print(f"   release_gating distribution: {gate}")
if no_s or no_a or no_g: fails.append("UX_TESTABLE_AND_GATED")

# ---- [4] UX_TRACES_TO_PROD --------------------------------------------------------------------
ptext=open(PROD,encoding="utf-8").read()
pids=sorted(int(m.group(1)) for m in re.finditer(r'(?m)^#{2,6}\s+REQ-PROD-(\d{3})\b',ptext))
ux2prod={}
for n,b in blocks.items():
    mref=re.search(r'\*\*references\*\*\s*:\s*(.+)',b)
    refs=sorted(set(int(x) for x in re.findall(r'REQ-PROD-(\d{3})',mref.group(1)))) if mref else []
    ux2prod[n]=refs
no_ref=[n for n,r in ux2prod.items() if not r]
bad=[(n,r) for n,rs in ux2prod.items() for r in rs if r not in pids]
covered=set(r for rs in ux2prod.values() for r in rs)
must=(set(range(30,37))|set(range(1,29))|{32,33,34,42}) & set(pids)
uncovered_must=sorted(must-covered)
print("\n[4] UX_TRACES_TO_PROD")
print(f"   REQ-PROD ids in register: {len(pids)} (expect 42)")
print(f"   REQ-UX with no REQ-PROD ref: {no_ref or 'NONE'} | refs to non-existent REQ-PROD: {bad or 'NONE'}")
print(f"   distinct REQ-PROD covered: {len(covered)} | must-cover set: {len(must)} | uncovered-among-must: {uncovered_must or 'NONE'}")
# forward trace must be clean; reverse uncovered-must are the recorded dispositions {15,23,24}
if no_ref or bad: fails.append("UX_TRACES_TO_PROD(forward)")
if sorted(uncovered_must) not in ([], [15,23,24]):
    fails.append(f"UX_TRACES_TO_PROD(reverse unexpected uncovered {uncovered_must})")

# ---- [5] COMPOSES_AGAINST_PARENT --------------------------------------------------------------
extra_fields=set()
for n,b in blocks.items():
    for fm in re.findall(r'(?m)^\s*-?\s*\*\*([a-z_]+)\*\*\s*:',b):
        if fm not in {"statement","acceptance_criteria","release_gating","references"}:
            extra_fields.add(fm)
print("\n[5] COMPOSES_AGAINST_PARENT")
print(f"   non-parent fields used: {sorted(extra_fields) or 'NONE (only statement/acceptance_criteria/release_gating/references)'}")
if extra_fields: fails.append("COMPOSES_AGAINST_PARENT")

# ---- [6] SURFACE_COVERAGE ---------------------------------------------------------------------
surfaces={
 "first_visit_landing":r'Landing',"sign_up":r'Sign up',"sign_in":r'Sign in',
 "account_recovery":r'Recover access|recover',"sign_out":r'Sign out',
 "home_timeline":r'Home timeline',"compose_and_post":r'Compose|Posting and conversation',
 "reply_and_conversation":r'conversation',"like_unlike":r'\bLike\b',"follow_unfollow":r'[Ff]ollow',
 "discovery_find_people":r'discover|find people|Discovery',"view_profile":r'[Pp]rofile',
 "onboarding_empty_state":r'Onboarding',"edit_profile":r'Edit profile',
 "account_settings":r'Settings hub|/settings',"data_export":r'Export your data|/settings/export',
 "account_deletion":r'Delete account|/settings/delete',"notifications":r'Notifications',
 "report_and_block":r'Report|Block',"help_support_entry":r'Help & support',
 "considered_states_global":r'Empty, loading, and error states',
}
print("\n[6] SURFACE_COVERAGE")
miss_surf=[k for k,rx in surfaces.items() if not re.search(rx,doc)]
print(f"   required surfaces present: {len(surfaces)-len(miss_surf)}/{len(surfaces)} | absent: {miss_surf or 'NONE'}")
if miss_surf: fails.append("SURFACE_COVERAGE")

# ---- [7] NOT_SKELETAL -------------------------------------------------------------------------
screens_region=doc[doc.index("## Screens and flows"):doc.index("## Visual language and design system")]
states_blocks=len(re.findall(r'\*\*States\.?\*\*|States:',screens_region))
empty=len(re.findall(r'(?i)\bempty\b',screens_region)); err=len(re.findall(r'(?i)\berror\b',screens_region)); load=len(re.findall(r'(?i)\bloading\b',screens_region))
screen_heads=len(re.findall(r'(?m)^####? ',screens_region))
print("\n[7] NOT_SKELETAL (screens region)")
print(f"   screen/sub headings:{screen_heads} states-markers:{states_blocks} empty:{empty} error:{err} loading:{load}")
if not (states_blocks>=10 and empty>20 and err>20 and load>20): fails.append("NOT_SKELETAL")

# ---- [8] HYGIENE ------------------------------------------------------------------------------
pat=re.compile(r'100\.90\.75\.93|\bssh\b|kubectl|\bk3d\b|argocd|tailscale|/home/|SUBTASK_|taskflow/dags|_GLOBAL|_BRIEF|proc-[0-9a-f]|design-chirp-r1|Co-Authored|Generated with|🤖|claude\.com|anthropic|noreply@|\bc805525\b|mattsmcknight|mattm@',re.I)
hits=[(i+1,l.strip()[:90]) for i,l in enumerate(doc.splitlines()) if pat.search(l)]
print("\n[8] HYGIENE")
print(f"   forbidden-token hits: {hits[:20] if hits else 'NONE'}")
if hits: fails.append("HYGIENE")

print("\n"+"="*78)
print("GATE RESULT:", "ALL IDENTITIES PASS" if not fails else f"FAILURES: {fails}")
print("="*78)
sys.exit(1 if fails else 0)
