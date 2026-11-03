import re,json
def clean(t):
    t=re.sub(r'<ref[^>]*/>','',t); t=re.sub(r'<ref.*?</ref>','',t,flags=re.S)
    t=re.sub(r'\{\{sortname\|([^|}]*)\|([^|}]*)[^}]*\}\}',r'\1 \2',t)
    t=re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]',r'\1',t)
    t=re.sub(r'\{\{small\|([^}]*)\}\}',r'\1',t,flags=re.I)
    t=re.sub(r'<br\s*/?>',' ',t); t=re.sub(r'\{\{[^}]*\}\}','',t); t=re.sub(r"'''?","",t)
    return re.sub(r'\s+',' ',t).strip()
def rows(txt):
    parts=re.split(r'\n(?:\|-[^\n]*\n)+',txt)
    for p in parts:
        m=re.match(r'\s*!\s*(?:rowspan="?\d+"?\s*\|)?\s*\{\{ushr\|(\w\w)\|(\w+)\|X\}\}',p)
        if m: yield m.group(1),m.group(2),p
main=open('main.wiki').read()
D={}
for st,dn,p in rows(main):
    cells=[c for c in re.split(r'\n\|',p)][1:]
    pvi=re.search(r'PVI\|(EVEN|[RD]\|\d+)',p,re.I)
    pv=pvi.group(1).upper().replace('|','+') if pvi else None
    inc=clean(cells[1]) if len(cells)>1 else ''
    pm=re.search(r'background-color:#[0-9A-Fa-f]{6}"?\s*\|\s*(Republican|Democratic|DFL|Independent)\b',p)
    party=pm.group(1) if pm else ''
    inc=clean(cells[1]) if len(cells)>1 and pm else (clean(cells[1]) if len(cells)>1 else '')
    cands=re.findall(r'\*\{\{Party stripe\|([^}]*)\}\}(.*)',p)
    cl=[(clean(n), pt) for pt,n in cands]
    dist=0 if dn=='AL' else int(dn)
    D[(st,dist)]=dict(state=st,district=dist,pvi=pv,incumbent=inc,inc_party_full=party,cands=cl)
rt=open('ratings.wiki').read()
R={}
for st,dn,p in rows(rt):
    rs=re.findall(r'\{\{USRaceRating\|([^}]*)\}\}',p)
    def norm(x):
        a=x.split('|')
        if a[0]=='Tossup': return 'Toss-up'
        lvl={'Safe':'Solid'}.get(a[0],a[0]); return f'{lvl} {a[1]}'
    rs=[norm(x) for x in rs]
    dist=0 if dn=='AL' else int(dn)
    R[(st,dist)]=rs[:3]
print(len(D),len(R))
json.dump({'D':[dict(v) for v in D.values()],'R':{f'{k[0]}-{k[1]}':v for k,v in R.items()}},open('parsed.json','w'))
import collections
print(collections.Counter(v['inc_party_full'] for v in D.values()).most_common(8))
print(list(D.values())[0]); print(D.get(('TX',15)))
