import json,os,sys,urllib.request,urllib.error,random
ENV_URL=os.environ["MAKEFUN_ENV_URL"]
NODE_BUDGET=int(os.environ.get("NODE_BUDGET",10**5))
_TB=b'"\'"&\n	\r &	 \r,,*\'(&+-""!  \n\r'
MGV=[82,337,365,477,1025,0];EGV=[94,281,297,512,936,0];PHI=[0,1,1,2,4,0]
PM=[[0]*128 for _ in range(13)];PE=[[0]*128 for _ in range(13)]
for _t in range(6):
 for _i in range(64):
  _r,_f=_i//8,_i%8;_s=_r*16+_f
  PM[_t+7][_s]=(_TB[_t*64+(_i^56)]-22)*8+MGV[_t];PE[_t+7][_s]=(_TB[384+_t*64+(_i^56)]-22)*8+EGV[_t]
  PM[5-_t][_s^112]=-PM[_t+7][_s];PE[5-_t][_s^112]=-PE[_t+7][_s]
_R=random.Random(0x5EED)
ZP=[[_R.getrandbits(64) for _ in range(128)] for _ in range(13)]
ZW=_R.getrandbits(64);ZC=[_R.getrandbits(64) for _ in range(16)];ZE=[_R.getrandbits(64) for _ in range(8)]
CM={4:12,0:13,7:14,116:3,112:7,119:11}
CS=[(1,4,6,(5,6),7,4,(4,5,6)),(2,4,2,(3,2,1),0,4,(4,3,2)),(4,116,118,(117,118),119,-4,(116,117,118)),(8,116,114,(115,114,113),112,-4,(116,115,114))]
VAL=[0,100,320,330,500,900,0]
KN=(-33,-31,-18,-14,14,18,31,33);KG=(-17,-16,-15,-1,1,15,16,17);DG=(-17,-15,15,17);OT=(-16,-1,1,16)
MATE=100000
class K:
 def __init__(S):
  S.A=[0]*128;S.W=1;S.C=0;S.E=-1;S.H=0;S.Y={1:4,-1:116};S.I=[];S.J=[];S.Z=0;S.MG=0;S.EG=0;S.PH=0
 def F(S,fen):
  p=fen.split();S.A=[0]*128;S.MG=0;S.EG=0;S.PH=0;S.Z=0
  for ri,row in enumerate(p[0].split("/")):
   r=7-ri;f=0
   for ch in row:
    if ch.isdigit():f+=int(ch)
    else:
     pc="PNBRQK".index(ch.upper())+1
     if ch.islower():pc=-pc
     sq=r*16+f;S.A[sq]=pc;S.MG+=PM[pc+6][sq];S.EG+=PE[pc+6][sq];S.Z^=ZP[pc+6][sq]
     if abs(pc)!=1:S.PH+=PHI[abs(pc)-1]
     if abs(pc)==6:S.Y[1 if pc>0 else-1]=sq
     f+=1
  S.PH=min(S.PH,24);S.W=1 if p[1]=="w"else-1
  if S.W==-1:S.Z^=ZW
  S.C=sum((1<<i)for i,c in enumerate("KQkq")if c in(p[2]if len(p)>2 else""))
  S.Z^=ZC[S.C];S.E=-1
  if len(p)>3 and p[3]!="-":
   S.E=(ord(p[3][0])-97)+(int(p[3][1])-1)*16;S.Z^=ZE[S.E&7]
  S.H=int(p[4])if len(p)>4 else 0;S.I=[];S.J=[S.Z]
 def T(S,sq,by):
  A=S.A
  for s in(sq-15*by,sq-17*by):
   if not(s&0x88)and A[s]==by:return True
  for o in KN:
   s=sq+o
   if not(s&0x88)and A[s]==2*by:return True
  for o in KG:
   s=sq+o
   if not(s&0x88)and A[s]==6*by:return True
  for o in DG:
   s=sq+o
   while not(s&0x88):
    q=A[s]
    if q:
     if q==3*by or q==5*by:return True
     break
    s+=o
  for o in OT:
   s=sq+o
   while not(s&0x88):
    q=A[s]
    if q:
     if q==4*by or q==5*by:return True
     break
    s+=o
  return False
 def G(S,co=False):
  A,W=S.A,S.W;n=[];d=16 if W==1 else-16;sr=1 if W==1 else 6;pr=6 if W==1 else 1
  for sq in range(128):
   if sq&0x88:continue
   p=A[sq]
   if p==0 or(p>0)!=(W==1):continue
   t=abs(p);r=sq>>4
   if t==1:
    if not co or r==pr:
     s=sq+d
     if A[s]==0:
      if r==pr:
       for q in(5,4,3,2):n.append((sq,s,q))
      elif not co:
       n.append((sq,s,0))
       if r==sr:
        x=sq+2*d
        if A[x]==0:n.append((sq,x,0))
    for df in(-1,1):
     s=sq+d+df
     if s&0x88:continue
     q=A[s]
     if q and(q>0)!=(W==1):
      if r==pr:
       for q2 in(5,4,3,2):n.append((sq,s,q2))
      else:n.append((sq,s,0))
     elif s==S.E:n.append((sq,s,0))
   elif t==2 or t==6:
    offs=KN if t==2 else KG
    for o in offs:
     s=sq+o
     if s&0x88:continue
     q=A[s]
     if q==0:
      if not co:n.append((sq,s,0))
     elif(q>0)!=(W==1):n.append((sq,s,0))
    if t==6 and not co:
     for bit,kf,kt,em,rf,rp,path in CS:
      if S.C&bit and sq==kf and all(A[s]==0 for s in em)and A[rf]==rp and not any(S.T(s,-W)for s in path):n.append((kf,kt,0))
   else:
    offs=[]
    if t==3 or t==5:offs+=DG
    if t==4 or t==5:offs+=OT
    for o in offs:
     s=sq+o
     while not(s&0x88):
      q=A[s]
      if q==0:
       if not co:n.append((sq,s,0))
      else:
       if(q>0)!=(W==1):n.append((sq,s,0))
       break
      s+=o
  return n
 def M(S,mv):
  f,t,pr=mv;A=S.A;pc=A[f];cap=A[t];e=-1
  if abs(pc)==1 and t==S.E and not A[t]:
   e=t-16 if S.W==1 else t+16;cap=A[e]
  S.I.append((mv,cap,e,S.C,S.E,S.H,S.MG,S.EG,S.PH,S.Z))
  if e>=0:
   A[e]=0;S.MG-=PM[cap+6][e];S.EG-=PE[cap+6][e];S.Z^=ZP[cap+6][e]
  elif cap:
   S.MG-=PM[cap+6][t];S.EG-=PE[cap+6][t];S.Z^=ZP[cap+6][t]
   if abs(cap)!=1:S.PH-=PHI[abs(cap)-1]
  S.MG-=PM[pc+6][f];S.EG-=PE[pc+6][f];S.Z^=ZP[pc+6][f]
  q=pr*S.W if pr else pc
  if pr:S.PH+=PHI[pr-1]
  A[t]=q;A[f]=0;S.MG+=PM[q+6][t];S.EG+=PE[q+6][t];S.Z^=ZP[q+6][t]
  if abs(pc)==6 and abs(t-f)==2:
   rf=t+1 if t&15==6 else t-2;rt=t-1 if t&15==6 else t+1;rp=4 if t<16 else-4
   A[rt],A[rf]=rp,0;S.MG+=PM[rp+6][rt]-PM[rp+6][rf];S.EG+=PE[rp+6][rt]-PE[rp+6][rf];S.Z^=ZP[rp+6][rf]^ZP[rp+6][rt]
  if abs(pc)==6:S.Y[S.W]=t
  o=S.C;S.C&=CM.get(f,15)&CM.get(t,15);S.Z^=ZC[o]^ZC[S.C]
  o=S.E;S.E=(f+t)//2 if abs(pc)==1 and abs(t-f)==32 else-1
  if o!=-1:S.Z^=ZE[o&7]
  if S.E!=-1:S.Z^=ZE[S.E&7]
  S.H=0 if abs(pc)==1 or cap else S.H+1;S.W=-S.W;S.Z^=ZW;S.J.append(S.Z)
  return not S.T(S.Y[-S.W],S.W)
 def U(S):
  mv,cap,e,c,ep,h,mg,eg,ph,z=S.I.pop()
  f,t,pr=mv;A=S.A;S.W=-S.W;pc=A[t]
  A[f]=(1 if S.W==1 else-1)if pr else pc;A[t]=cap if e<0 else 0
  if e>=0:A[e]=cap
  if abs(pc)==6 and abs(t-f)==2:
   rf=t+1 if t&15==6 else t-2;rt=t-1 if t&15==6 else t+1;rp=4 if t<16 else-4;A[rt],A[rf]=0,rp
  if abs(pc)==6:S.Y[S.W]=f
  S.C,S.E,S.H=c,ep,h;S.MG,S.EG,S.PH,S.Z=mg,eg,ph,z;S.J.pop()
 def L(S):
  S.I.append((None,0,-1,S.C,S.E,S.H,S.MG,S.EG,S.PH,S.Z))
  if S.E!=-1:S.Z^=ZE[S.E&7]
  S.E=-1;S.H+=1;S.W=-S.W;S.Z^=ZW;S.J.append(S.Z)
 def D(S):
  _,_,_,c,ep,h,mg,eg,ph,z=S.I.pop()
  S.W=-S.W;S.E,S.H=ep,h;S.MG,S.EG,S.PH,S.Z=mg,eg,ph,z;S.J.pop()
 def P(S):
  o=[]
  for mv in S.G():
   if S.M(mv):o.append(mv)
   S.U()
  return o
 def V(S):
  mg=S.MG;eg=S.EG;ph=min(S.PH,24)
  s=(mg*ph+eg*(24-ph))//24
  return s if S.W==1 else-s
TT={};KL={};ND=[0];AB=[False]
def O(b,n,u=None,ply=0):
 def key(mv):
  f,t,pr=mv;s=0;cap=b.A[t]
  if cap:s+=10000+VAL[abs(cap)]*10-VAL[abs(b.A[f])]//10
  if pr:s+=9000+VAL[pr]
  if u and mv==u:s+=100000
  k=KL.get(ply)
  if k and mv in k:s+=5000
  return-s
 return sorted(n,key=key)
def Q(b,a,w,ply):
 ND[0]+=1
 if ND[0]>NODE_BUDGET:AB[0]=True;return 0
 if b.H>=100:return 0
 if ply>64:return b.V()
 c=b.T(b.Y[b.W],-b.W)
 if not c:
  st=b.V()
  if st>=w:return st
  if st>a:a=st
 x=-MATE-1 if c else a
 for mv in O(b,b.G(co=not c),ply=ply):
  if not b.M(mv):b.U();continue
  s=-Q(b,-w,-a,ply+1);b.U()
  if AB[0]:return 0
  if s>x:x=s
  if s>=w:return s
  if s>a:a=s
 if c and x==-MATE-1:return-MATE+ply
 return x
def S(b,d,a,w,ply):
 if b.H>=100:return 0
 if b.Z in b.J[:-1]:return 0
 c=b.T(b.Y[b.W],-b.W)
 if c:d+=1
 if d<=0:return Q(b,a,w,ply)
 ND[0]+=1
 if ND[0]>NODE_BUDGET:AB[0]=True;return 0
 a0=a;u=None;ent=TT.get(b.Z)
 if ent:
  s,fl,mv,ed=ent
  if ed>=d:
   s=s-ply if s>MATE-1000 else s+ply if s<-MATE+1000 else s
   if fl==0:return s
   if fl==1 and s>=w:return s
   if fl==2 and s<=a:return s
  u=mv
 if d>=3 and not c and b.V()>=w:
  b.L();s=-S(b,d-3,-w,-w+1,ply+1);b.D()
  if AB[0]:return 0
  if s>=w:return w
 n=O(b,b.G(),u,ply);x=-MATE-1;v=None
 for ix,mv in enumerate(n):
  cap=b.A[mv[1]];ep=b.E
  if not b.M(mv):b.U();continue
  red=1 if d>=3 and ix>=3 and not c and not cap and mv[1]!=ep and not mv[2] else 0
  if ix==0:s=-S(b,d-1,-w,-a,ply+1)
  else:
   s=-S(b,d-1-red,-a-1,-a,ply+1)
   if a<s<w:s=-S(b,d-1,-w,-a,ply+1)
  b.U()
  if AB[0]:return 0
  if s>x:x=s;v=mv
  if s>a:a=s
  if a>=w:
   k=KL.setdefault(ply,[])
   if mv not in k:k.insert(0,mv);del k[2:]
   break
 if x==-MATE-1:return-MATE+ply if b.T(b.Y[b.W],-b.W)else 0
 TT[b.Z]=(x+ply if x>MATE-1000 else x-ply if x<-MATE+1000 else x,2 if x<=a0 else 1 if x>=w else 0,v,d)
 return x
def R(b,legal):
 v=legal[0];ND[0]=0;AB[0]=False
 for d in range(1,13):
  if AB[0]:break
  a=-MATE-1;cb=v;cs=-MATE-1
  for mv in O(b,legal,v,0):
   if not b.M(mv):b.U();continue
   s=-S(b,d-1,-MATE-1,-a,1);b.U()
   if AB[0]:break
   if s>cs:cs=s;cb=mv
   if s>a:a=s
  if AB[0]:break
  v=cb
  if cs>MATE-1000:break
 return v
def X(mv):
 f,t,pr=mv
 s="abcdefgh"[f&7]+str((f>>4)+1)+"abcdefgh"[t&7]+str((t>>4)+1)
 if pr:s+="nbrq"[pr-2]
 return s
def y(b,u):
 f=(ord(u[0])-97)+(int(u[1])-1)*16;t=(ord(u[2])-97)+(int(u[3])-1)*16;pr="nbrq".index(u[4])+2 if len(u)==5 else 0
 for mv in b.G():
  if mv[0]==f and mv[1]==t and mv[2]==pr:b.M(mv);return True
 return False
def p(path,body):
 req=urllib.request.Request(ENV_URL+path,data=json.dumps(body).encode(),headers={"content-type":"application/json"})
 try:
  with urllib.request.urlopen(req)as res:return json.load(res)
 except urllib.error.HTTPError as e:sys.exit(e.code)
def m():
 b=K();hist=K();started=False;applied=0
 while True:
  g=p("/game",{})
  if g["status"]=="done":break
  if not started:
   hist.F(g["start_fen"]);applied=0;started=True;TT.clear();KL.clear()
  while applied<len(g["moves"]):
   y(hist,g["moves"][applied]);applied+=1
  b.F(g["fen"]);b.J=list(hist.J)
  while g["status"]=="your_move":
   legal=b.P();env_legal=set(g["legal_moves"]);ours=[mv for mv in legal if X(mv)in env_legal]
   mv=R(b,ours if ours else legal)
   g=p("/move",{"game":g["game"],"move":X(mv)})
   if g["status"]=="your_move":
    while applied<len(g["moves"]):
     y(hist,g["moves"][applied]);applied+=1
    b.F(g["fen"]);b.J=list(hist.J)
  started=False
 return g
m()
