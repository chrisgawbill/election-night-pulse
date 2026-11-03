import json,re,os
P=json.load(open('parsed.json'))
NAMES={'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan','MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin','WY':'Wyoming'}
PM={'Republican':'R','Democratic':'D','DFL':'D','Independent':'I'}
raw=json.load(open('house_raw.json')) if os.path.exists('house_raw.json') else {}
civic={}
for st,rs in raw.items():
    for r in rs:
        m=re.search(r'US House (\d+)$',r['election_name']) ; 
        if m: civic[(st,int(m.group(1)))]=r['id']
        elif re.search(r'US House( At-Large)?$',r['election_name']): civic[(st,0)]=r['id']
rows=[]
for x in P['D']:
    st=x['state']
    if st not in NAMES: continue
    d=x['district']; rid=f"{st}-{'AL' if d==0 else str(d).zfill(2)}"
    inc=x['incumbent']
    ip=PM.get(x['inc_party_full'])
    if st=='MN' and not ip and inc and 'None' not in inc and 'Vacant' not in inc: ip='D'
    if 'Kiley' in inc: ip='I'
    if re.search(r'None \(new seat\)|Vacant',inc): inc=('Vacant' if 'Vacant' in inc else 'New seat'); ip=None
    inc=re.sub(r'colspan=\d+\s*\|','',inc).split(' Redistricted')[0].strip()
    dem=rep=None; oth=[]
    for name,pt in x['cands']:
        nm=re.sub(r'\s*\((Democratic|Republican|DFL)\)$','',name).strip()
        if pt.startswith('Democratic') or 'DFL' in pt or 'Democratic–Farmer–Labor' in pt:
            dem = dem or nm
        elif pt.startswith('Republican'): rep = rep or nm
        else: oth.append(name)
    rt=P['R'].get(f'{st}-{d}')
    cook=rt[0] if rt else None
    if not cook:
        pv=x['pvi'] or ''
        side = ip if ip in ('D','R') else ('D' if pv.startswith('D') else 'R')
        cook='Solid '+side
    rows.append(dict(race_id=rid,state=st,state_name=NAMES[st],district=d,office='U.S. House '+rid,incumbent=inc or None,inc_party=ip,
        dem=dem,rep=rep,other=', '.join(oth[:3]) or None,pvi=x['pvi'],cook=cook,
        inside_elections=rt[1] if rt and len(rt)>1 else None,sabato=rt[2] if rt and len(rt)>2 else None,
        rated_competitive=bool(rt),civic_id=civic.get((st,d))))
rows.sort(key=lambda r:(r['state'],r['district']))
json.dump(rows,open('house.json','w'),indent=0)
import collections
print(len(rows), collections.Counter(r['cook'] for r in rows), collections.Counter(r['inc_party'] for r in rows), sum(1 for r in rows if r['civic_id']))
print([r for r in rows if r['race_id'] in('TX-15','MN-02','CA-06','FL-20')])
