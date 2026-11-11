import re, json
frags = [
 ('prod','SUBTASK_release_bar/SUBTASK_bar_prod/outputs/bar-prod.md'),
 ('dom','SUBTASK_release_bar/SUBTASK_bar_dom/outputs/bar-dom.md'),
 ('ux','SUBTASK_release_bar/SUBTASK_bar_ux/outputs/bar-ux.md'),
 ('id','SUBTASK_release_bar/SUBTASK_bar_id/outputs/bar-id.md'),
 ('ops','SUBTASK_release_bar/SUBTASK_bar_ops/outputs/bar-ops.md'),
]
hdr=re.compile(r'^(#{3,4})\s*(BAR-\d{3})\b(.*)$',re.M)
# a field value: text after '- **name**:' up to next '- **', or a line starting with #, or '---', or EOF
STOP=re.compile(r'\n(?=-\s*\*\*)|\n(?=#)|\n---|\Z')
def field(block,name):
    m=re.search(r'-\s*\*\*%s\*\*\s*:\s*'%name,block)
    if not m: return None
    rest=block[m.end():]
    stop=STOP.search(rest)
    val=rest[:stop.start()] if stop else rest
    return re.sub(r'\s+',' ',val).strip()

bars={}; order=[]
for area,f in frags:
    txt=open(f).read()
    ms=list(hdr.finditer(txt))
    for i,m in enumerate(ms):
        bid=m.group(2); title=m.group(3).strip(' —-')
        s=m.end(); e=ms[i+1].start() if i+1<len(ms) else len(txt)
        block=txt[s:e]
        bars[bid]=dict(area=area,title=title,
                       statement=field(block,'statement'),
                       references=re.findall(r'REQ-[A-Z]+-\d{3}',field(block,'references') or ''),
                       method=field(block,'verification_method'))
        order.append(bid)

# reuse validated proposed stages
bm=json.load(open('SUBTASK_release_bar/SUBTASK_bar_synthesis/calculations/barmap.json'))
for bid in bars: bars[bid]['proposed']=bm['stage'][bid]

# FINAL staging moves (proposal -> final), each documented
to_early = {'BAR-016','BAR-113','BAR-010'} | {f'BAR-{n}' for n in (130,131,132,133,134,135,136,137,138,139,141,143,144,145)}
moves=[]
for bid,b in bars.items():
    fs=b['proposed']
    if bid in to_early and b['proposed']!='usable_early':
        fs='usable_early'; moves.append((bid,b['proposed'],fs))
    b['final']=fs

from collections import Counter,defaultdict
final={b:bars[b]['final'] for b in bars}
print("FINAL distribution:",dict(Counter(final.values())),"total",len(bars))
print("moves:",len(moves))
byarea=defaultdict(Counter)
for b in bars.values(): byarea[b['area']][b['final']]+=1
for area,_ in frags: print("  ",area,dict(byarea[area]))
# verify every bar: statement present, method in vocab, >=1 ref, final staged
VOCAB={'manual_user_check','automated_test','inspection','operational_check'}
probs=[]
for bid,b in bars.items():
    if not b['statement']: probs.append(bid+" no statement")
    if b['method'] not in VOCAB: probs.append(bid+" method="+str(b['method']))
    if not b['references']: probs.append(bid+" no refs")
    if b['final'] not in ('usable_early','releasable'): probs.append(bid+" stage")
print("post-parse problems:", probs if probs else "NONE")
json.dump(bars,open('SUBTASK_release_bar/SUBTASK_bar_synthesis/calculations/bars_final.json','w'))
print("ok")
