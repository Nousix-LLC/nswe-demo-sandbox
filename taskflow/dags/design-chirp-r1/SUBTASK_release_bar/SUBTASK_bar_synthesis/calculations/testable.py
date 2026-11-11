import re
frags = {
 'prod':'SUBTASK_release_bar/SUBTASK_bar_prod/outputs/bar-prod.md',
 'dom' :'SUBTASK_release_bar/SUBTASK_bar_dom/outputs/bar-dom.md',
 'ux'  :'SUBTASK_release_bar/SUBTASK_bar_ux/outputs/bar-ux.md',
 'id'  :'SUBTASK_release_bar/SUBTASK_bar_id/outputs/bar-id.md',
 'ops' :'SUBTASK_release_bar/SUBTASK_bar_ops/outputs/bar-ops.md',
}
VOCAB={'manual_user_check','automated_test','inspection','operational_check'}
STAGES={'usable_early','releasable'}
hdr=re.compile(r'^#{3,4}\s*(BAR-\d{3})\b',re.M)
problems=[]
stage_map={}   # bar -> proposed stage
method_map={}
refs_map={}
for area,f in frags.items():
    txt=open(f).read()
    ms=list(hdr.finditer(txt))
    for i,m in enumerate(ms):
        bid=m.group(1); s=m.end(); e=ms[i+1].start() if i+1<len(ms) else len(txt)
        block=txt[s:e]
        refs=set(re.findall(r'REQ-[A-Z]+-\d{3}',block))
        vm=re.search(r'verification_method\*{0,2}:?\*{0,2}\s*:?\s*([a-z_]+)',block)
        st=re.search(r'(?:proposed_stage|stage)\*{0,2}:?\*{0,2}\s*:?\s*([a-z_]+)',block)
        vmv=vm.group(1) if vm else None
        stv=st.group(1) if st else None
        if not refs: problems.append(f"{bid}: no REQ reference")
        if vmv not in VOCAB: problems.append(f"{bid}: bad/missing verification_method={vmv}")
        if stv not in STAGES: problems.append(f"{bid}: bad/missing stage={stv}")
        refs_map[bid]=refs; method_map[bid]=vmv; stage_map[bid]=stv
print("defined bars:",len(stage_map))
print("BAR_TESTABLE problems:", problems if problems else "NONE -> PASS")
print()
# proposed staging distribution
from collections import Counter
c=Counter(stage_map.values())
print("proposed stage distribution:", dict(c))
ue=sorted(b for b,s in stage_map.items() if s=='usable_early')
print("proposed usable_early count:",len(ue))
print("proposed usable_early:", ", ".join(ue))
# save maps for reuse
import json
json.dump({'stage':stage_map,'method':method_map,'refs':{k:sorted(v) for k,v in refs_map.items()}},
          open('SUBTASK_release_bar/SUBTASK_bar_synthesis/calculations/barmap.json','w'))
