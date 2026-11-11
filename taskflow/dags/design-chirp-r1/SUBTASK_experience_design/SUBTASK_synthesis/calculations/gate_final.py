#!/usr/bin/env python3
"""Full verification gate over the ASSEMBLED experience-design.md. Emits recorded evidence
for all eight subtree identities."""
import re, json

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_experience_design"
DOC  = BASE + "/outputs/experience-design.md"
PROD = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1/SUBTASK_product_requirements/outputs/product-requirements.md"

doc = open(DOC, encoding="utf-8").read()

RANGES = [("ia_interaction",1,19),("visual_system",20,39),("screens_flows",40,89),
          ("responsive",90,99),("accessibility",100,119)]
def owner_of(n):
    for o,lo,hi in RANGES:
        if lo<=n<=hi: return o,lo,hi
    return None,None,None

# ---- parse REQ-UX register from the consolidated section --------------------------------------
reg_start = doc.index("## Requirements and acceptance criteria")
reg = doc[reg_start:]
HEAD = re.compile(r'^####\s+REQ-UX-(\d{3})\b', re.M)
heads = [(m.start(), int(m.group(1))) for m in HEAD.finditer(reg)]
blocks = {}
for i,(pos,num) in enumerate(heads):
    end = heads[i+1][0] if i+1<len(heads) else len(reg)
    blocks[num] = reg[pos:end]

nums = sorted(blocks)
print("="*78); print("GATE OVER ASSEMBLED experience-design.md"); print("="*78)

# ---- IDENTITY 1: SECTION_COVERAGE -------------------------------------------------------------
order = ["## Information architecture and interaction model","## Screens and flows",
         "## Empty, loading, and error states","## Visual language and design system",
         "## Responsive layout","## Accessibility","## Requirements and acceptance criteria"]
pos = []
ok_once = True
for h in order:
    c = len(re.findall(r'(?m)^'+re.escape(h)+r'\s*$', doc))
    if c!=1: ok_once=False
    pos.append(doc.index(h))
print("\n[1] SECTION_COVERAGE")
print("  seven required sections, each exactly once:", ok_once)
print("  in contract order:", pos==sorted(pos))

# ---- IDENTITY 2: ID_UNIQUE_IN_RANGE -----------------------------------------------------------
missing = sorted(set(range(1,120))-set(nums)); extra = sorted(set(nums)-set(range(1,120)))
oor = [n for n in nums if not (owner_of(n)[1] <= n <= owner_of(n)[2])]
dups = len(heads)-len(set(n for _,n in heads))
print("\n[2] ID_UNIQUE_IN_RANGE")
print("  count:",len(nums)," contiguous 1..119:", nums==list(range(1,120)),
      " missing:",missing or "NONE"," extra:",extra or "NONE"," dup-headings:",dups," out-of-range:",oor or "NONE")

# ---- IDENTITY 3: UX_TESTABLE_AND_GATED --------------------------------------------------------
no_s=[];no_a=[];no_g=[]
gate={"true":0,"false":0}
for n,b in blocks.items():
    if not re.search(r'\*\*statement\*\*\s*:',b): no_s.append(n)
    if not re.search(r'\*\*acceptance_criteria\*\*\s*:',b): no_a.append(n)
    mg=re.search(r'\*\*release_gating\*\*\s*:\s*(true|false)',b)
    if not mg: no_g.append(n)
    else: gate[mg.group(1)]+=1
print("\n[3] UX_TESTABLE_AND_GATED")
print("  missing statement:",no_s or "NONE"," missing acceptance_criteria:",no_a or "NONE"," missing gate-flag:",no_g or "NONE")
print("  release_gating distribution:",gate)

# ---- IDENTITY 4: UX_TRACES_TO_PROD ------------------------------------------------------------
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
print("  REQ-UX with no REQ-PROD ref:",no_ref or "NONE"," refs to non-existent REQ-PROD:",bad or "NONE")
print("  distinct REQ-PROD covered:",len(covered)," must-cover set size:",len(must))
print("  uncovered among must-cover:",uncovered_must or "NONE","  (dispositions recorded in SYNTHESIS)")

# ---- IDENTITY 5: COMPOSES_AGAINST_PARENT ------------------------------------------------------
# parent field set exactly {id-by-heading, statement, acceptance_criteria, release_gating, references(trace)}
extra_fields=set()
for n,b in blocks.items():
    for fm in re.findall(r'(?m)^- \*\*([a-z_]+)\*\*\s*:',b):
        if fm not in {"statement","acceptance_criteria","release_gating","references"}:
            extra_fields.add(fm)
print("\n[5] COMPOSES_AGAINST_PARENT")
print("  non-parent fields used in any REQ-UX:",sorted(extra_fields) or "NONE (only statement/acceptance_criteria/release_gating/references)")

# ---- IDENTITY 8: HYGIENE ----------------------------------------------------------------------
pat=re.compile(r'100\.90\.75\.93|\bssh\b|kubectl|k3d|argocd|tailscale|/home/|SUBTASK_|taskflow/dags|_GLOBAL|_BRIEF|proc-[0-9a-f]|design-chirp-r1|Co-Authored|Generated with|🤖|claude|anthropic|noreply@|c805525',re.I)
hits=[(i+1,l) for i,l in enumerate(doc.splitlines()) if pat.search(l)]
print("\n[8] HYGIENE")
print("  forbidden-token hits:",hits[:20] if hits else "NONE")

# ---- IDENTITY 6: SURFACE_COVERAGE (presence of each required surface in the assembled doc) -----
surfaces={
 "first_visit_landing":r'Landing',
 "sign_up":r'Sign up',"sign_in":r'Sign in',"account_recovery":r'Recover access',"sign_out":r'Sign out',
 "home_timeline":r'Home timeline',"compose_and_post":r'Posting and conversation|Compose',
 "reply_and_conversation":r'conversation',"like_unlike":r'\bLike\b',"follow_unfollow":r'[Ff]ollow',
 "discovery_find_people":r'discover|find people|Discovery',"view_profile":r'profile',
 "onboarding_empty_state":r'Onboarding',"edit_profile":r'Edit profile',"account_settings":r'Settings hub|/settings',
 "data_export":r'Export your data|/settings/export',"account_deletion":r'Delete account|/settings/delete',
 "notifications":r'Notifications',"report_and_block":r'Report|Block',"help_support_entry":r'Help & support',
 "considered_states_global":r'Empty, loading, and error states',
}
print("\n[6] SURFACE_COVERAGE (designed-with-states presence in the assembled doc)")
miss_surf=[]
for k,rx in surfaces.items():
    present=bool(re.search(rx,doc))
    if not present: miss_surf.append(k)
    print(f"  {k:28s} {'present' if present else 'ABSENT'}")
print("  absent surfaces:",miss_surf or "NONE")

# ---- IDENTITY 7: NOT_SKELETAL (screens carry States / empty / error / loading) -----------------
# count '**States.**' / 'Empty' / 'Error' / 'Loading' structures in the screens+states sections
screens_region=doc[doc.index("## Screens and flows"):doc.index("## Visual language and design system")]
states_blocks=len(re.findall(r'\*\*States\.\*\*|States:',screens_region))
empty=len(re.findall(r'(?i)\bempty\b',screens_region)); err=len(re.findall(r'(?i)\berror\b',screens_region)); load=len(re.findall(r'(?i)\bloading\b',screens_region))
screen_heads=len(re.findall(r'(?m)^####? ',screens_region))
print("\n[7] NOT_SKELETAL (screens region)")
print(f"  screen/sub headings:{screen_heads}  '**States.**' markers:{states_blocks}  empty-mentions:{empty}  error:{err}  loading:{load}")
