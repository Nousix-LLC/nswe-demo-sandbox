import re, sys
areas = {
 'PROD': ('SUBTASK_product_requirements/outputs/product-requirements.md',
          'SUBTASK_release_bar/SUBTASK_bar_prod/outputs/bar-prod.md'),
 'DOM':  ('SUBTASK_domain_app_design/outputs/domain-application-design.md',
          'SUBTASK_release_bar/SUBTASK_bar_dom/outputs/bar-dom.md'),
 'UX':   ('SUBTASK_experience_design/outputs/experience-design.md',
          'SUBTASK_release_bar/SUBTASK_bar_ux/outputs/bar-ux.md'),
 'ID':   ('SUBTASK_identity_trust/outputs/identity-security.md',
          'SUBTASK_release_bar/SUBTASK_bar_id/outputs/bar-id.md'),
 'OPS':  ('SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md',
          'SUBTASK_release_bar/SUBTASK_bar_ops/outputs/bar-ops.md'),
}

def gating_set(doc, area):
    """Walk REQ blocks; a block is gating if its release_gating line within the block says true."""
    txt = open(doc).read()
    # split on requirement headers
    hdr = re.compile(r'^#{2,4}\s*(REQ-%s-\d{3})\b' % area, re.M)
    gat = re.compile(r'release_gating\*{0,2}:?\*{0,2}\s*:?\s*(true|false)', re.I)
    matches = list(hdr.finditer(txt))
    g=set(); allreq=set()
    for i,m in enumerate(matches):
        rid=m.group(1); allreq.add(rid)
        start=m.end(); end = matches[i+1].start() if i+1<len(matches) else len(txt)
        block=txt[start:end]
        gm=gat.search(block)
        if gm and gm.group(1).lower()=='true':
            g.add(rid)
    return g, allreq

def referenced_set(frag, area):
    txt=open(frag).read()
    # only count ids on '- **references**:' lines (the authoritative per-bar refs)
    ref=set()
    for line in txt.splitlines():
        if re.search(r'\*\*references\*\*', line):
            ref|=set(re.findall(r'REQ-%s-\d{3}' % area, line))
    return ref

print(f"{'AREA':5} {'gating':7} {'referenced':11} {'uncovered gating':s}")
ok=True
for area,(doc,frag) in areas.items():
    g,allreq=gating_set(doc,area)
    ref=referenced_set(frag,area)
    uncovered=sorted(g-ref)
    if uncovered: ok=False
    print(f"{area:5} {len(g):<7} {len(ref):<11} {uncovered if uncovered else 'NONE  (all gating covered)'}")
    # also report gating reqs: note which non-gating got a bar (allowed, informational)
print()
print("OVERALL GATING_REQ_COVERAGE:", "PASS" if ok else "FAIL")
