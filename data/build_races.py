import json
N={'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan','MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire','NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OK':'Oklahoma','OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota','TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia','WI':'Wisconsin','WY':'Wyoming'}
R={'Sol R':'Solid R','Saf R':'Solid R','Lik R':'Likely R','Ln R':'Lean R','Tlt R':'Lean R','TU':'Toss-up','Ln D':'Lean D','Ln D†':'Lean D','Tlt D':'Lean D','Tlt D†':'Lean D','Lik D':'Likely D','Lik D†':'Likely D','Sol D':'Solid D','Saf D':'Solid D','Sol D†':'Solid D','Saf D†':'Solid D','Lik D†':'Likely D'}
# state, special, incumbent, inc_party, dem, rep, other, cook, ie, sabato
S=[('AL',0,'Tommy Tuberville (retiring)','R','Everett Wess','Barry Moore','','Sol R','Sol R','Saf R'),
('AK',0,'Dan Sullivan','R','Mary Peltola','Dan Sullivan','','TU','TU','Ln D†'),
('AR',0,'Tom Cotton','R','Hallie Shoffner','Tom Cotton','Jeff Wadlin (L)','Sol R','Sol R','Saf R'),
('CO',0,'John Hickenlooper','D','John Hickenlooper','Mark Baisley','','Sol D','Sol D','Saf D'),
('DE',0,'Chris Coons','D','Chris Coons','Michael Katz','','Sol D','Sol D','Saf D'),
('FL',1,'Ashley Moody (appointed)','R','Angie Nixon','Ashley Moody','Neil Gillespie (I)','Lik R','Lik R','Lik R'),
('GA',0,'Jon Ossoff','D','Jon Ossoff','Mike Collins','','Lik D','Lik D','Lik D'),
('ID',0,'Jim Risch','R','','Jim Risch','Todd Achilles (I)','Sol R','Sol R','Saf R'),
('IL',0,'Dick Durbin (retiring)','D','Juliana Stratton','Don Tracy','','Sol D','Sol D','Saf D'),
('IA',0,'Joni Ernst (retiring)','R','Josh Turek','Ashley Hinson','','TU','TU','Ln R'),
('KS',0,'Roger Marshall','R','Adam Hamilton','Roger Marshall','','TU','TU','Ln D†'),
('KY',0,'Mitch McConnell (retiring)','R','Charles Booker','Andy Barr','','Sol R','Sol R','Saf R'),
('LA',0,'Bill Cassidy (lost primary)','R','Jamie Davis','Julia Letlow','','Sol R','Lik R','Ln R'),
('ME',0,'Susan Collins','R','Troy Jackson','Susan Collins','','TU','TU','Ln D†'),
('MA',0,'Ed Markey','D','Ed Markey','John Deaton','','Sol D','Sol D','Saf D'),
('MI',0,'Gary Peters (retiring)','D','Abdul El-Sayed','Mike Rogers','','Ln D','Tlt D','Ln D'),
('MN',0,'Tina Smith (retiring)','D','Peggy Flanagan','Michele Tafoya','','Ln D','Ln D','Lik D'),
('MS',0,'Cindy Hyde-Smith','R','Scott Colom','Cindy Hyde-Smith','Ty Pinkins (I)','Lik R','Lik R','Lik R'),
('MT',0,'Steve Daines (retiring)','R','Alani Bankhead','Kurt Alme','Seth Bodnar (I)','Sol R','Sol R','Saf R'),
('NE',0,'Pete Ricketts','R','','Pete Ricketts','Dan Osborn (I)','Ln R','Tlt R','Ln R'),
('NH',0,'Jeanne Shaheen (retiring)','D','Chris Pappas','John E. Sununu','','Ln D','Tlt D','Lik D'),
('NJ',0,'Cory Booker','D','Cory Booker','Justin Murphy','','Sol D','Sol D','Saf D'),
('NM',0,'Ben Ray Luján','D','Ben Ray Luján','Larry Marker','','Sol D','Sol D','Saf D'),
('NC',0,'Thom Tillis (retiring)','R','Roy Cooper','Michael Whatley','','Lik D†','Ln D†','Lik D†'),
('OH',1,'Jon Husted (appointed)','R','Sherrod Brown','Jon Husted','','TU','Tlt D†','Ln D†'),
('OK',0,'Alan Armstrong (appointed, retiring)','R',"N'Kiyla Thomas",'Kevin Hern','','Sol R','Sol R','Saf R'),
('OR',0,'Jeff Merkley','D','Jeff Merkley','David Smith','','Sol D','Sol D','Saf D'),
('RI',0,'Jack Reed','D','Jack Reed','Raymond McKay','','Sol D','Sol D','Saf D'),
('SC',0,'Darline Graham (appointed)','R','Annie Andrews','Darline Graham','Kasie Whitener (L)','Ln R','Tlt R','Ln R'),
('SD',0,'Mike Rounds','R','','Mike Rounds','Brian Bengs (I)','Sol R','Sol R','Saf R'),
('TN',0,'Bill Hagerty','R','Marquita Bradshaw','Bill Hagerty','','Sol R','Sol R','Saf R'),
('TX',0,'John Cornyn (lost primary)','R','James Talarico','Ken Paxton','Ted Brown (L)','TU','Tlt D†','Ln D†'),
('VA',0,'Mark Warner','D','Mark Warner','Bert Mizusawa','','Sol D','Sol D','Saf D'),
('WV',0,'Shelley Moore Capito','R','Rachel Fetty Anderson','Shelley Moore Capito','','Sol R','Sol R','Saf R'),
('WY',0,'Cynthia Lummis (retiring)','R','James Byrd','Harriet Hageman','','Sol R','Sol R','Saf R')]
G=[('AL','Kay Ivey (term-limited)','R','Doug Jones','Tommy Tuberville','Solid R','Solid R','Likely R'),
('AK','Mike Dunleavy (term-limited)','R','Jonathan Kreiss-Tomkins','Dave Bronson / Treg Taylor / Bernadette Wilson','Lean D','Tilt D','Likely D'),
('AZ','Katie Hobbs','D','Katie Hobbs','Andy Biggs','Likely D','Tilt D','Likely D'),
('AR','Sarah Huckabee Sanders','R','Fredrick Love','Sarah Huckabee Sanders','Solid R','Solid R','Safe R'),
('CA','Gavin Newsom (term-limited)','D','Xavier Becerra','Steve Hilton','Solid D','Solid D','Safe D'),
('CO','Jared Polis (term-limited)','D','Phil Weiser','Victor Marx','Solid D','Solid D','Safe D'),
('CT','Ned Lamont','D','Ned Lamont','Ryan Fazio','Solid D','Solid D','Safe D'),
('FL','Ron DeSantis (term-limited)','R','David Jolly','Byron Donalds','Lean R','Lean R','Lean R'),
('GA','Brian Kemp (term-limited)','R','Keisha Lance Bottoms','Rick Jackson','Tossup','Tilt D','Lean D'),
('HI','Josh Green','D','Josh Green','Gary Cordery','Solid D','Solid D','Safe D'),
('ID','Brad Little','R','Terri Pickens','Brad Little','Solid R','Solid R','Safe R'),
('IL','JB Pritzker','D','JB Pritzker','Darren Bailey','Solid D','Solid D','Safe D'),
('IA','Kim Reynolds (retiring)','R','Rob Sand','Zach Lahn','Lean D','Lean D','Lean D'),
('KS','Laura Kelly (term-limited)','D','Cindy Holscher','Ty Masterson','Tossup','Tilt R','Lean R'),
('ME','Janet Mills (term-limited)','D','Hannah Pingree','Robert B. Charles','Solid D','Solid D','Likely D'),
('MD','Wes Moore','D','Wes Moore','Dan Cox','Solid D','Solid D','Safe D'),
('MA','Maura Healey','D','Maura Healey','Mike Minogue','Solid D','Solid D','Safe D'),
('MI','Gretchen Whitmer (term-limited)','D','Jocelyn Benson','John James','Lean D','Lean D','Likely D'),
('MN','Tim Walz (retiring)','D','Amy Klobuchar','Lisa Demuth','Solid D','Likely D','Safe D'),
('NE','Jim Pillen','R','Lynne Walz','Jim Pillen','Lean R','Likely R','Likely R'),
('NV','Joe Lombardo','R','Aaron Ford','Joe Lombardo','Tossup','Tossup','Lean D'),
('NH','Kelly Ayotte','R','Cinde Warmington','Kelly Ayotte','Likely R','Solid R','Lean R'),
('NM','Michelle Lujan Grisham (term-limited)','D','Deb Haaland','Gregg Hull','Solid D','Likely D','Safe D'),
('NY','Kathy Hochul','D','Kathy Hochul','Bruce Blakeman','Solid D','Likely D','Safe D'),
('OH','Mike DeWine (term-limited)','R','Amy Acton','Vivek Ramaswamy','Lean D','Tilt D','Lean D'),
('OK','Kevin Stitt (term-limited)','R','Cyndi Munson','Mike Mazzei','Likely R','Likely R','Likely R'),
('OR','Tina Kotek','D','Tina Kotek','Christine Drazan','Lean D','Tilt D','Lean D'),
('PA','Josh Shapiro','D','Josh Shapiro','Stacy Garrity','Solid D','Solid D','Safe D'),
('RI','Dan McKee (lost primary)','D','Helena Foulkes','Aaron Guckian','Solid D','Solid D','Safe D'),
('SC','Henry McMaster (term-limited)','R','Jermaine Johnson','Alan Wilson','Solid R','Solid R','Safe R'),
('SD','Larry Rhoden','R','Dan Ahlers','Larry Rhoden','Solid R','Solid R','Safe R'),
('TN','Bill Lee (term-limited)','R','Jerri Green','Marsha Blackburn','Solid R','Likely R','Safe R'),
('TX','Greg Abbott','R','Gina Hinojosa','Greg Abbott','Lean R','Tilt R','Lean R'),
('VT','Phil Scott','R','Amanda Janoo','Phil Scott','Likely R','Likely R','Lean R'),
('WI','Tony Evers (retiring)','D','David Crowley','Tom Tiffany','Lean D','Tilt D','Lean D'),
('WY','Mark Gordon (term-limited)','R','Kenneth Casner','Eric Barlow','Solid R','Solid R','Safe R')]
def norm(x):
    if not x: return None
    x=x.replace('†','').strip()
    m={'Sol':'Solid','Saf':'Solid','Safe':'Solid','Lik':'Likely','Ln':'Lean','Tlt':'Tilt','TU':'Toss-up','Tossup':'Toss-up'}
    p=x.split()
    if p[0] in m: p[0]=m[p[0]]
    return ' '.join(p)
rows=[]
def add(**k):
    base=dict(status='Not called',winner_party=None,winner=None,dem_pct=None,rep_pct=None,other_pct=None,pct_reporting=None,called_by=None,result_updated=None)
    base.update(k); rows.append(base)
for st,sp,inc,ip,d,r,o,c,ie,sb in S:
    add(race_id=f'{st}-SEN'+('-SP' if sp else ''),state=st,state_name=N[st],office='U.S. Senate'+(' (special)' if sp else ''),chamber='Senate',level='Federal',
        incumbent=inc,inc_party=ip,dem=d or None,rep=r or None,other=o or None,cook=norm(c),inside_elections=norm(ie),sabato=norm(sb))
for st,inc,ip,d,r,c,ie,sb in G:
    add(race_id=f'{st}-GOV',state=st,state_name=N[st],office='Governor',chamber='Governor',level='State',
        incumbent=inc,inc_party=ip,dem=d,rep=r,other=None,cook=norm(c),inside_elections=norm(ie),sabato=norm(sb))
TX=[('TX-LTGOV','Lieutenant Governor','State','Dan Patrick','R','Vikki Goodwin','Dan Patrick','Anthony Cristo (L), Kevin McCormick (G)',None),
('TX-AG','Attorney General','State','Open (Ken Paxton ran for Senate)','R','Nathan Johnson','Mayes Middleton','Tom Oxford (L)','Likely R'),
('TX-COMP','Comptroller','State','Open','R','Sarah Eckhardt','Don Huffines','V. Alonzo Echavarria-Garza (L), Shehla Faizi (G)',None),
('TX-09','U.S. House TX-09','Federal',None,None,None,None,None,'Likely R'),
('TX-15','U.S. House TX-15','Federal','Monica De La Cruz','R','Bobby Pulido','Monica De La Cruz',None,'Toss-up'),
('TX-23','U.S. House TX-23','Federal','Open','R','Katy Padilla Stout','Brandon Herrera','Ben Mendoza (I)','Lean R'),
('TX-28','U.S. House TX-28','Federal',None,'D',None,None,None,'Likely D'),
('TX-34','U.S. House TX-34','Federal','Vicente Gonzalez','D','Vicente Gonzalez','Eric Flores','Chris Royal (L), Eddie Espinoza (G)','Lean D'),
('TX-35','U.S. House TX-35','Federal',None,None,None,None,None,'Toss-up')]
for rid,off,lvl,inc,ip,d,r,o,rt in TX:
    add(race_id=rid,state='TX',state_name='Texas',office=off,chamber='House' if 'House' in off else 'Texas statewide',level=lvl,
        incumbent=inc,inc_party=ip,dem=d,rep=r,other=o,cook=None,inside_elections=None,sabato=None,consensus_270=rt)
for x in rows: x.setdefault('consensus_270',None)
json.dump(rows,open('races.json','w'),indent=0)
print(len(rows), sorted(set(x['cook'] for x in rows if x['cook'])))
