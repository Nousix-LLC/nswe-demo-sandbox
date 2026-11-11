#!/usr/bin/env python3
# Mechanical assist for the judgment identities: SURFACE_COVERAGE, NOT_SKELETAL, COMPOSES_AGAINST_VOCAB.
# Reads the assembled Screens-and-flows section and reports, per designed screen, whether it carries
# layout / content / primary-action / the three states, and which component-library names it uses.
import re, os
BASE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
atext = open(f"{BASE}/outputs/screens-flows.md", encoding="utf-8").read()
lines = atext.splitlines()

# bound the "## Screens and flows" section (up to "## Empty, error, and loading states")
start = next(i for i,l in enumerate(lines) if re.match(r'^##\s+Screens and flows', l))
end   = next(i for i,l in enumerate(lines) if re.match(r'^##\s+Empty, error, and loading states', l))
sec = lines[start:end]

# designed-screen blocks = level-4 (####) headings within the section
heads = [(i,l) for i,l in enumerate(sec) if re.match(r'^####\s', l)]
print(f"Screens-and-flows section: lines {start+1}..{end+1}; {len(heads)} level-4 (####) screen/group headings:\n")

COMPONENTS = ["ChirpCard","ComposeBox","TextField","Toggle","PrimaryButton","SecondaryButton","IconButton",
              "NavShell","ListView","SettingRow","Dialog","Toast","InlineFeedback","InlineError",
              "EmptyState","LoadingState","Avatar","ProfileHeader"]

def block(i0):
    j = len(sec)
    for k in range(i0+1, len(sec)):
        if re.match(r'^####\s', sec[k]) or re.match(r'^#{1,3}\s', sec[k]):
            j = k; break
    return "\n".join(sec[i0:j])

rows = []
for i,l in heads:
    b = block(i)
    bl = b.lower()
    has_layout = "layout" in bl
    has_content = "content" in bl
    has_action = ("primary action" in bl) or ("primary-action" in bl)
    has_empty = "empty" in bl
    has_error = "error" in bl
    has_loading = "loading" in bl
    comps = sorted({c for c in COMPONENTS if c in b})
    rows.append((l.strip("# ").strip(), has_layout, has_content, has_action, has_empty, has_error, has_loading, len(comps)))

print(f"{'screen/group heading':<62} lay con act emp err load  #comp")
for name,la,co,ac,em,er,lo,nc in rows:
    flag = lambda x: ' Y ' if x else ' . '
    print(f"{name[:60]:<62}{flag(la)}{flag(co)}{flag(ac)}{flag(em)}{flag(er)}{flag(lo)}  {nc}")

# summary
skeletal = [r[0] for r in rows if not (r[1] and r[2] and r[3] and r[4] and r[5] and r[6])]
novocab  = [r[0] for r in rows if r[7] == 0]
print(f"\nscreens missing a layout/content/action/empty/error/loading marker: {skeletal or 'none'}")
print(f"screens referencing zero component-library names: {novocab or 'none'}")

# whole-section component usage + inventory route usage
print(f"\ncomponent-library names used in section: "
      f"{sorted({c for c in COMPONENTS if c in '\\n'.join(sec)})}")
routes = sorted(set(re.findall(r'`/[A-Za-z0-9:_/-]*`', "\n".join(sec))))
print(f"inventory routes referenced (sample): {routes[:20]}")
