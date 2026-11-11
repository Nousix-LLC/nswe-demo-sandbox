#!/usr/bin/env python3
"""Independent verification gate for the chirp release bar.

Re-derives every mechanical identity from the authoritative sources (the five
area design docs for the gating sets, the five BAR fragments for the criteria,
and the assembled release-bar.md for the final register/staging). Trusts no
prior intermediate. Prints a JSON verdict.
"""
import re, json

BASE = "/home/user/nousix-runtime/nswe-demo/taskflow/dags/design-chirp-r1"
RB = BASE + "/SUBTASK_release_bar"

AREA_DOCS = {
    'PROD': BASE + "/SUBTASK_product_requirements/outputs/product-requirements.md",
    'DOM':  BASE + "/SUBTASK_domain_app_design/outputs/domain-application-design.md",
    'UX':   BASE + "/SUBTASK_experience_design/outputs/experience-design.md",
    'ID':   BASE + "/SUBTASK_identity_trust/outputs/identity-security.md",
    'OPS':  BASE + "/SUBTASK_operational_readiness/SUBTASK_ops_synthesis/outputs/operational-readiness.md",
}
FRAGMENTS = {  # spoke -> (path, area-prefix, lo, hi)
    'prod': (RB + "/SUBTASK_bar_prod/outputs/bar-prod.md", 'PROD', 1, 99),
    'dom':  (RB + "/SUBTASK_bar_dom/outputs/bar-dom.md",   'DOM', 100, 199),
    'ux':   (RB + "/SUBTASK_bar_ux/outputs/bar-ux.md",     'UX', 200, 299),
    'id':   (RB + "/SUBTASK_bar_id/outputs/bar-id.md",     'ID', 300, 399),
    'ops':  (RB + "/SUBTASK_bar_ops/outputs/bar-ops.md",   'OPS', 400, 499),
}
RELEASE_BAR = RB + "/outputs/release-bar.md"
VMETHODS = {'manual_user_check', 'automated_test', 'inspection', 'operational_check'}
STAGES = {'usable_early', 'releasable'}


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read().split('\n')


def parse_gating(path, area):
    lines = read(path)
    hdr = re.compile(r'^#### (REQ-' + area + r'-\d{3})\b')
    heads = [(i, m.group(1)) for i, l in enumerate(lines) for m in [hdr.match(l)] if m]
    allreq, gating, nongating, noflag = set(), set(), set(), set()
    for idx, (i, rid) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        rg = None
        for bl in lines[i:end]:
            mm = re.match(r'^- \*\*release_gating\*\*:\s*(true|false)', bl)
            if mm:
                rg = mm.group(1)
                break
        allreq.add(rid)
        if rg == 'true':
            gating.add(rid)
        elif rg == 'false':
            nongating.add(rid)
        else:
            noflag.add(rid)
    return allreq, gating, nongating, noflag


def parse_fragment(path):
    lines = read(path)
    bar = re.compile(r'^### (BAR-\d{3})\b')
    heads = [(i, m.group(1)) for i, l in enumerate(lines) for m in [bar.match(l)] if m]
    out = {}
    for idx, (i, bid) in enumerate(heads):
        end = heads[idx + 1][0] if idx + 1 < len(heads) else len(lines)
        refs, vm, ps, stmt = set(), None, None, None
        for bl in lines[i:end]:
            m = re.match(r'^- \*\*references\*\*:\s*(.+)', bl)
            if m:
                refs |= set(re.findall(r'REQ-[A-Z]+-\d{3}', m.group(1)))
            m = re.match(r'^- \*\*verification_method\*\*:\s*([a-z_]+)', bl)
            if m:
                vm = m.group(1)
            m = re.match(r'^- \*\*proposed_stage\*\*:\s*([a-z_]+)', bl)
            if m:
                ps = m.group(1)
            m = re.match(r'^- \*\*statement\*\*:\s*(.+)', bl)
            if m:
                stmt = m.group(1).strip()
        out[bid] = {'refs': sorted(refs), 'vm': vm, 'proposed_stage': ps, 'statement': stmt}
    return out


def parse_release_bar(path):
    lines = read(path)
    pat = re.compile(r'^\*\*(BAR-\d{3})\*\*\s*\(`([a-z_]+)`\s*·\s*`([a-z_]+)`\)\s*[—-]+\s*(.*?)\s*_Enforces\s+(.+?)\._\s*$')
    out = {}
    for l in lines:
        m = pat.match(l)
        if m:
            bid, stage, vm, stmt, refstr = m.groups()
            refs = sorted(set(re.findall(r'REQ-[A-Z]+-\d{3}', refstr)))
            out[bid] = {'stage': stage, 'vm': vm, 'statement': stmt, 'refs': refs}
    # section headers (## level)
    secs = [l[3:].strip() for l in lines if l.startswith('## ') and not l.startswith('###')]
    return out, secs


def num(bid):
    return int(bid.split('-')[1])


report = {'identities': {}, 'counts': {}, 'problems': []}

# ---- parse everything
gating = {}
area_all = {}
for area, path in AREA_DOCS.items():
    allr, g, ng, nf = parse_gating(path, area)
    gating[area] = g
    area_all[area] = allr
    report['counts'][f'{area}_req_total'] = len(allr)
    report['counts'][f'{area}_gating'] = len(g)
    report['counts'][f'{area}_nongating'] = len(ng)
    if nf:
        report['problems'].append(f'{area}: {len(nf)} REQ headings with no release_gating flag: {sorted(nf)[:10]}')

frag_bars = {}
all_bar = {}
for spoke, (path, area, lo, hi) in FRAGMENTS.items():
    fb = parse_fragment(path)
    frag_bars[spoke] = fb
    for bid, rec in fb.items():
        all_bar.setdefault(bid, []).append(spoke)

rb_bars, rb_secs = parse_release_bar(RELEASE_BAR)

# ---- Identity 1: BAR_RANGE_RESPECTED
range_viol = []
for spoke, (path, area, lo, hi) in FRAGMENTS.items():
    for bid in frag_bars[spoke]:
        if not (lo <= num(bid) <= hi):
            range_viol.append(f'{bid} in {spoke} outside {lo}..{hi}')
report['identities']['BAR_RANGE_RESPECTED'] = 'PASS' if not range_viol else f'FAIL: {range_viol}'

# ---- Identity 2: NO_BAR_COLLISION
collisions = {b: s for b, s in all_bar.items() if len(s) > 1}
total_defined = sum(len(v) for v in frag_bars.values())
distinct = len(all_bar)
report['counts']['bar_defined_in_fragments'] = total_defined
report['counts']['bar_distinct'] = distinct
report['identities']['NO_BAR_COLLISION'] = 'PASS' if not collisions else f'FAIL: {collisions}'

# ---- Identity 4: BAR_TESTABLE (fragments are authoritative for method+refs)
testable_viol = []
for spoke, fb in frag_bars.items():
    for bid, rec in fb.items():
        if rec['vm'] not in VMETHODS:
            testable_viol.append(f'{bid}: bad/missing vm {rec["vm"]!r}')
        if not rec['refs']:
            testable_viol.append(f'{bid}: no REQ reference')
report['identities']['BAR_TESTABLE'] = 'PASS' if not testable_viol else f'FAIL: {testable_viol}'

# ---- Identity 3: GATING_REQ_COVERAGE (per area, against area doc gating set)
referenced_all = set()
for fb in frag_bars.values():
    for rec in fb.values():
        referenced_all |= set(rec['refs'])
coverage = {}
cov_fail = []
for area, g in gating.items():
    uncovered = sorted(g - referenced_all)
    coverage[area] = {'gating': len(g), 'uncovered': uncovered}
    if uncovered:
        cov_fail.append(f'{area}: {len(uncovered)} uncovered gating REQ: {uncovered}')
report['coverage'] = coverage
report['counts']['gating_total'] = sum(len(g) for g in gating.values())
report['identities']['GATING_REQ_COVERAGE'] = 'PASS' if not cov_fail else f'FAIL: {cov_fail}'

# ---- Identity 5: BAR_STAGED (release-bar is authoritative for final stage)
stage_viol = []
for bid, rec in rb_bars.items():
    if rec['stage'] not in STAGES:
        stage_viol.append(f'{bid}: bad stage {rec["stage"]!r}')
stage_counts = {'usable_early': 0, 'releasable': 0}
for rec in rb_bars.values():
    if rec['stage'] in stage_counts:
        stage_counts[rec['stage']] += 1
report['counts']['stage_usable_early'] = stage_counts['usable_early']
report['counts']['stage_releasable'] = stage_counts['releasable']
report['identities']['BAR_STAGED'] = 'PASS' if not stage_viol else f'FAIL: {stage_viol}'

# ---- Cross-check: fragment BAR set == release-bar BAR set, content preserved
frag_ids = set(all_bar)
rb_ids = set(rb_bars)
missing_in_rb = sorted(frag_ids - rb_ids)
extra_in_rb = sorted(rb_ids - frag_ids)
content_drift = []
for bid in sorted(frag_ids & rb_ids):
    fspoke = all_bar[bid][0]
    frec = frag_bars[fspoke][bid]
    rrec = rb_bars[bid]
    if set(frec['refs']) != set(rrec['refs']):
        content_drift.append(f'{bid}: refs frag={frec["refs"]} rb={rrec["refs"]}')
    if frec['vm'] != rrec['vm']:
        content_drift.append(f'{bid}: vm frag={frec["vm"]} rb={rrec["vm"]}')
    # statement preserved (exact)
    if frec['statement'] != rrec['statement']:
        content_drift.append(f'{bid}: statement differs')
report['crosscheck'] = {
    'missing_in_release_bar': missing_in_rb,
    'extra_in_release_bar': extra_in_rb,
    'content_drift_count': len(content_drift),
    'content_drift_sample': content_drift[:20],
}

# ---- Identity 7: THREE_SECTIONS_PRESENT
report['release_bar_sections'] = rb_secs
want = ['mvp_vs_releasable', 'release', 'completeness']  # loose keywords in order
ok_secs = len(rb_secs) == 3
report['identities']['THREE_SECTIONS_PRESENT'] = 'PASS' if ok_secs else f'FAIL: sections={rb_secs}'

print(json.dumps(report, indent=2))
